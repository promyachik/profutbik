"""
PROMYACHIK — ЧЕТВЁРТЫЙ ШАГ: ГРАФИК ДИНАМИЧЕСКОЙ СТОИМОСТИ

Собирает объект игрока для `static/js/transfer-player-market-value-chart.js`
из настоящей истории оценок Transfermarkt.

История лежит на открытом API: `/player/<id>/market-value-history`.
Раньше считалось, что взять её неоткуда — страничный `ceapi` закрыт WAF,
и графики строились руками из двух-трёх точек. Этот путь свободен и отдаёт
всю карьеру: у Родри 29 оценок с 2016 года, с датами, клубами и возрастом.

Все точки в график не идут: разметка рассчитана на горсть подписей и
эмблем, 29 штук на 320 пикселей превратятся в кашу. Отбирается смысловой
костяк — первая оценка, текущая, пик карьеры и приход в каждый клуб.

    python market_value_chart.py --check rodri-real-madrid
    python market_value_chart.py --add rodri-real-madrid --save
    python market_value_chart.py --add-missing --save
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import re
import ssl
import struct
import sys
import urllib.request
from datetime import datetime
from pathlib import Path

BIN = Path(__file__).resolve().parent
sys.path.insert(0, str(BIN))
from transfer_discovery import ACTIVE_PROJECT  # noqa: E402
from transfer_enrichment import api  # noqa: E402
from job_builder import compact_money  # noqa: E402

CHART_JS = ACTIVE_PROJECT / "static" / "js" / "transfer-player-market-value-chart.js"
SINGLE_HTML = ACTIVE_PROJECT / "layouts" / "transfers" / "single.html"
TRANSFERS_DIR = ACTIVE_PROJECT / "content" / "transfers"
CLUBS_DIR = ACTIVE_PROJECT / "content" / "clubs"
CLUB_LOGOS = ACTIVE_PROJECT / "data" / "club-logos.json"

# Сколько точек показываем. У утверждённых 50 графиков разброс 2–8,
# типичное значение 5. Держимся той же плотности.
MAX_POINTS = 7

TM_CREST_URL = "https://tmssl.akamaized.net/images/wappen/homepageWappen150x150/%s.png"
CHART_LOGO_DIR = Path("images") / "clubs" / "chart"

MONTHS_RU = ["янв.", "фев.", "мар.", "апр.", "май", "июнь",
             "июль", "авг.", "сен.", "окт.", "ноя.", "дек."]


# ---------------------------------------------------------------------------
# История оценок
# ---------------------------------------------------------------------------

def market_history(player_id: str) -> list[dict]:
    """Оценки Transfermarkt по возрастанию даты. Записи без суммы отбрасываем."""
    payload = api("/player/%s/market-value-history" % player_id)
    rows = ((payload or {}).get("data") or {}).get("history") or []
    clean = []
    for row in rows:
        money = row.get("marketValue") or {}
        determined = money.get("determined") or ""
        if not money.get("value") or not determined:
            continue
        clean.append({
            "date": determined,
            "season": row.get("seasonId"),
            "club_id": str(row.get("clubId") or ""),
            "value": int(money["value"]),
            "compact": money.get("compact") or {},
        })
    clean.sort(key=lambda item: item["date"])
    return clean


def select_points(history: list[dict], cap: int = MAX_POINTS) -> list[dict]:
    """Смысловой костяк истории: чем менялась карьера, а не каждый пересчёт.

    Порядок важности: последняя оценка (она же текущая цена), первая,
    пик карьеры, приход в каждый клуб от свежих к ранним, затем самые
    крупные изменения. Это те точки, из-за которых график вообще читают.
    """
    if len(history) <= cap:
        return history

    keep: list[int] = []

    def add(index: int) -> None:
        if index not in keep and len(keep) < cap:
            keep.append(index)

    add(len(history) - 1)
    add(0)
    add(max(range(len(history)), key=lambda i: history[i]["value"]))

    # Первая оценка в каждом клубе — момент перехода.
    arrivals = []
    previous = None
    for index, row in enumerate(history):
        if row["club_id"] and row["club_id"] != previous:
            arrivals.append(index)
        previous = row["club_id"]
    for index in reversed(arrivals):
        add(index)

    # Остаток добиваем самыми резкими скачками.
    jumps = sorted(range(1, len(history)),
                   key=lambda i: abs(history[i]["value"] - history[i - 1]["value"]),
                   reverse=True)
    for index in jumps:
        add(index)

    return [history[i] for i in sorted(keep)]


def label_points(points: list[dict]) -> list[str]:
    """Год, а если в году больше одной выбранной точки — месяц с годом."""
    years = [point["date"][:4] for point in points]
    labels = []
    for point, year in zip(points, years):
        if years.count(year) == 1:
            labels.append(year)
            continue
        month = MONTHS_RU[int(point["date"][5:7]) - 1]
        labels.append("%s %s" % (month, year))
    return labels


def money_label(compact: dict) -> str:
    """€55,00 млн -> €55 млн. Ровные суммы пишем без нулевого хвоста."""
    text = compact_money(compact)
    return text.replace(",00 ", " ") if text else ""


# ---------------------------------------------------------------------------
# Клубы точек
# ---------------------------------------------------------------------------

def club_index() -> dict[str, dict]:
    """id клуба Transfermarkt -> данные нашей клубной страницы."""
    index = {}
    if not CLUBS_DIR.exists():
        return index
    for directory in sorted(CLUBS_DIR.iterdir()):
        page = directory / "index.md"
        if not page.is_file():
            continue
        text = page.read_text(encoding="utf-8", errors="replace")
        tm_id = re.search(r'(?m)^transfermarkt_club_id:\s*"(\d+)"', text)
        if not tm_id:
            continue
        api_id = re.search(r'(?m)^api_football_id:\s*"(\d+)"', text)
        logo = re.search(r'(?m)^club_logo:\s*"([^"]*)"', text)
        name = re.search(r'(?m)^club_name:\s*"([^"]*)"', text)
        code = re.search(r'(?m)^club_code:\s*"([^"]*)"', text)
        index[tm_id.group(1)] = {
            "slug": directory.name,
            "name": name.group(1) if name else directory.name,
            "api_id": int(api_id.group(1)) if api_id else None,
            "logo": logo.group(1) if logo else "",
            "short": code.group(1) if code else "",
        }
    return index


def fetch_crest(tm_club_id: str) -> str:
    """Герб клуба с Transfermarkt для точки графика. Пусто при неудаче."""
    try:
        request = urllib.request.Request(
            TM_CREST_URL % tm_club_id, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(
                request, timeout=25, context=ssl.create_default_context()) as response:
            raw = response.read()
    except Exception as error:
        print("       герб клуба %s не получен: %s" % (tm_club_id, str(error)[:50]))
        return ""
    if raw[:8] != b"\x89PNG\r\n\x1a\n" or len(raw) < 2048:
        return ""
    width, height = struct.unpack(">II", raw[16:24])
    if width < 100 or height < 100:
        return ""
    relative = (CHART_LOGO_DIR / ("tm-%s.png" % tm_club_id)).as_posix()
    target = ACTIVE_PROJECT / "static" / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(raw)
    return relative


def short_code(name: str) -> str:
    words = [w for w in re.split(r"[\s.-]+", name) if w]
    if len(words) >= 3:
        return "".join(w[0] for w in words[:3]).upper()
    return (words[0][:3].upper() if words else "")


def resolve_club(tm_club_id: str, history: list[dict], index: dict) -> dict:
    """Клуб точки: имя, эмблема, период. Ничего не угадываем.

    Свои 148 страниц дают проверенную эмблему и id API-Football. Для клуба
    вне их — имя из API Transfermarkt, герб с его же CDN по id. Так на
    каждой точке оказывается настоящая эмблема, а не пустой кружок.
    """
    known = index.get(tm_club_id)
    seasons = sorted({row["season"] for row in history
                      if row["club_id"] == tm_club_id and row["season"]})
    if seasons:
        current = history[-1]["club_id"] == tm_club_id
        period = ("с %d" % seasons[0] if current
                  else "%d–%d" % (seasons[0], seasons[-1]) if seasons[0] != seasons[-1]
                  else str(seasons[0]))
    else:
        period = ""

    if known:
        return {"slug": known["slug"], "name": known["name"],
                "short": known["short"] or short_code(known["name"]),
                "api_id": known["api_id"], "period": period,
                "logo": known["logo"]}

    try:
        name = (api("/club/%s" % tm_club_id).get("data") or {}).get("name") or ""
    except Exception:
        name = ""
    if not name:
        name = "Клуб %s" % tm_club_id
    return {"slug": "tm-%s" % tm_club_id, "name": name, "short": short_code(name),
            "api_id": None, "period": period, "logo": fetch_crest(tm_club_id)}


# ---------------------------------------------------------------------------
# Сборка объекта игрока
# ---------------------------------------------------------------------------

def transfer_meta(slug: str) -> dict:
    page = TRANSFERS_DIR / slug / "index.md"
    if not page.is_file():
        raise SystemExit("нет страницы трансфера: %s" % slug)
    text = page.read_text(encoding="utf-8", errors="replace")

    def field(name: str) -> str:
        found = re.search(r'(?m)^%s:\s*"?([^"\n]*)"?\s*$' % name, text)
        return found.group(1).strip() if found else ""

    return {"slug": slug, "player": field("player"),
            "tm_id": field("transfermarkt_player_id"),
            "url": field("url") or "/transfers/%s/" % slug}


def build_player(slug: str, index: dict) -> dict | None:
    meta = transfer_meta(slug)
    if not meta["tm_id"]:
        print("  %s: нет transfermarkt_player_id, пропуск" % slug)
        return None

    history = market_history(meta["tm_id"])
    if len(history) < 2:
        print("  %s: оценок %d — для графика мало" % (slug, len(history)))
        return None

    chosen = select_points(history)
    labels = label_points(chosen)
    clubs: dict[str, dict] = {}
    points = []
    for row, label in zip(chosen, labels):
        value_label = money_label(row["compact"])
        if not value_label:
            print("  %s: непонятная сумма %r, точка пропущена" % (slug, row["compact"]))
            continue
        club_id = row["club_id"]
        if club_id not in clubs:
            clubs[club_id] = resolve_club(club_id, history, index)
        points.append({"label": label, "value_label": value_label,
                       "value": round(row["value"] / 1_000_000, 2),
                       "club": clubs[club_id]})

    if len(points) < 2:
        print("  %s: после отбора осталось %d точек" % (slug, len(points)))
        return None

    key = re.sub(r"[^a-z0-9]+", "-", meta["player"].lower()).strip("-") or slug
    print("  %s: оценок в истории %d, в график %d (%s → %s)"
          % (slug, len(history), len(points),
             points[0]["value_label"], points[-1]["value_label"]))
    return {"key": key, "name": meta["player"], "paths": [meta["url"]], "points": points}


# ---------------------------------------------------------------------------
# Запись в скрипт графика
# ---------------------------------------------------------------------------

def load_players() -> tuple[str, list[dict], tuple[int, int]]:
    text = CHART_JS.read_text(encoding="utf-8")
    found = re.search(r"(?m)^(\s*const PLAYERS = )(\[.*\])(;\s*)$", text)
    if not found:
        raise SystemExit("не нашёл массив PLAYERS в %s" % CHART_JS)
    return text, json.loads(found.group(2)), found.span(2)


def save_players(text: str, players: list[dict], span: tuple[int, int]) -> None:
    payload = json.dumps(players, ensure_ascii=False, separators=(", ", ": "))
    CHART_JS.write_text(text[:span[0]] + payload + text[span[1]:], encoding="utf-8")


def bump_cache_token() -> str:
    """Без свежего токена браузер отдаст старый скрипт и графика не будет.

    Отдельная строка проекта: проверка «объект есть в PLAYERS» ничего не
    доказывает, пока не сменился ?v= в layouts/transfers/single.html.
    """
    token = "mv" + datetime.now().strftime("%m%d%H%M%S")
    text = SINGLE_HTML.read_text(encoding="utf-8")
    new, count = re.subn(
        r"(transfer-player-market-value-chart\.js\?v=)[^\"']+",
        lambda m: m.group(1) + token, text, count=1)
    if not count:
        raise SystemExit("не нашёл cache-token графика в %s" % SINGLE_HTML)
    SINGLE_HTML.write_text(new, encoding="utf-8")
    return token


def charted_paths(players: list[dict]) -> set[str]:
    return {path for player in players for path in player["paths"]}


def missing_slugs(players: list[dict]) -> list[str]:
    have = charted_paths(players)
    return [directory.name for directory in sorted(TRANSFERS_DIR.iterdir())
            if (directory / "index.md").is_file()
            and "/transfers/%s/" % directory.name not in have]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Promyachik market value chart")
    parser.add_argument("--add", help="slug трансфера")
    parser.add_argument("--add-missing", action="store_true",
                        help="все страницы трансферов без графика")
    parser.add_argument("--check", help="показать историю, ничего не записывая")
    parser.add_argument("--save", action="store_true")
    args = parser.parse_args(argv)

    text, players, span = load_players()
    print("  в PLAYERS сейчас: %d\n" % len(players))

    if args.check:
        meta = transfer_meta(args.check)
        history = market_history(meta["tm_id"])
        print("  %s (TM %s): оценок %d" % (meta["player"], meta["tm_id"], len(history)))
        for row in history:
            print("     %s  season %s  club %-7s %s"
                  % (row["date"], row["season"], row["club_id"], money_label(row["compact"])))
        chosen = select_points(history)
        print("\n  в график пойдут %d:" % len(chosen))
        for row, label in zip(chosen, label_points(chosen)):
            print("     %-12s %s" % (label, money_label(row["compact"])))
        return 0

    targets = [args.add] if args.add else missing_slugs(players) if args.add_missing else []
    if not targets:
        parser.error("нужен --add, --add-missing или --check")

    index = club_index()
    added = 0
    for slug in targets:
        built = build_player(slug, index)
        if not built:
            continue
        players = [p for p in players if p["paths"] != built["paths"]]
        players.append(built)
        added += 1

    if not args.save:
        print("\n  пробный прогон, ничего не записано (добавьте --save)")
        return 0
    if not added:
        print("\n  добавлять нечего")
        return 0

    save_players(text, players, span)
    print("\n  в PLAYERS стало: %d" % len(players))
    print("  cache-token графика: %s" % bump_cache_token())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
