"""
PROMYACHIK — ДОГОН ПРОПУЩЕННОГО ТРАНСФЕРНОГО ОКНА

Ленты хранят сутки, поэтому переходы старше пары дней разведка не видит
никогда. После закрытия окна 1 сентября у нас оказалось 328 сделок мимо
сайта — при том что все они лежат в составах клубов на Transfermarkt.

Здесь второй источник разведки, независимый от RSS: обход составов по дате
прихода игрока. Ловит всё, что ленты пропустили, и годится как для догона,
так и для регулярной сверки.

Оговорка по правилу проекта: факт перехода обычно берётся из СМИ, а
Transfermarkt только подтверждает. Для догона медийного заголовка уже не
существует, поэтому источником на странице честно указывается Transfermarkt.

    python backfill_window.py --scan --from 2026-08-20 --to 2026-09-02
    python backfill_window.py --seed --min-value 15
"""
from __future__ import annotations

import argparse
import json
import sys
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path

BIN = Path(__file__).resolve().parent
sys.path.insert(0, str(BIN))
from paths import PARSER_ROOT, SITE, ensure_dirs  # noqa: E402
from transfer_discovery import slugify  # noqa: E402
from transfer_enrichment import api, squad_players, site_tm_ids  # noqa: E402

# Консоль на машине Дмитрия работает в cp1251 и падает на «Mickaël Nadé» —
# прогон обрывался на середине списка из-за одной буквы в имени.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

SCAN_FILE = PARSER_ROOT / "state" / "backfill_scan.json"
RECORDS_DIR = PARSER_ROOT / "state" / "records"


def club_pages() -> list[tuple[str, str, str]]:
    """(tm_club_id, имя клуба, лига) со страниц, которые у нас уже есть."""
    import re
    out = []
    root = SITE / "content" / "clubs"
    if not root.exists():
        return out
    for directory in sorted(root.iterdir()):
        page = directory / "index.md"
        if not page.is_file():
            continue
        text = page.read_text(encoding="utf-8", errors="replace")
        tm = re.search(r'(?m)^transfermarkt_club_id:\s*"(\d+)"', text)
        name = re.search(r'(?m)^club_name:\s*"([^"]*)"', text)
        league = re.search(r'(?m)^league:\s*"([^"]*)"', text)
        if tm:
            out.append((tm.group(1), name.group(1) if name else directory.name,
                        league.group(1) if league else ""))
    return out


def scan(date_from: str, date_to: str) -> list[dict]:
    """Кто пришёл в клуб в этом окне. Дата берётся из clubAssignments."""
    known = site_tm_ids()
    found: list[dict] = []
    clubs = club_pages()
    print("  клубов к обходу: %d | TM ID уже на сайте: %d" % (len(clubs), len(known)))
    for index, (club_id, club_name, league) in enumerate(clubs, 1):
        try:
            players = squad_players(club_id)
        except Exception:
            continue
        if index % 25 == 0:
            print("  ... обойдено: %d" % index, flush=True)
        for person in players:
            for assignment in (person.get("clubAssignments") or []):
                if assignment.get("type") != "current":
                    continue
                start = (assignment.get("start") or "")[:10]
                if date_from <= start <= date_to:
                    pid = str(person.get("id"))
                    value = ((person.get("marketValueDetails") or {}).get("current")
                             or {}).get("value") or 0
                    found.append({
                        "tm_player_id": pid,
                        "player_full_name": person.get("name") or "",
                        "to_club": club_name,
                        "tm_to_club_id": club_id,
                        "league": league,
                        "start": start,
                        "value_eur": int(value),
                        "on_site": pid in known,
                    })
    found.sort(key=lambda x: -x["value_eur"])
    ensure_dirs()
    SCAN_FILE.write_text(json.dumps(found, ensure_ascii=False, indent=1), encoding="utf-8")
    return found


def previous_club(tm_player_id: str, current_club_id: str) -> str:
    """Прежний клуб из истории стоимости: там у каждой оценки записан клуб.

    В карточке игрока прежнего клуба нет, а история оценок хранит клуб на
    момент каждой переоценки — последний отличный от нынешнего и есть тот,
    откуда игрок пришёл.
    """
    try:
        rows = (api("/player/%s/market-value-history" % tm_player_id)
                .get("data") or {}).get("history") or []
    except Exception:
        return ""
    for row in reversed(rows):
        cid = str(row.get("clubId") or "")
        if cid and cid != str(current_club_id):
            try:
                return (api("/club/%s" % cid).get("data") or {}).get("name") or ""
            except Exception:
                return ""
    return ""


# PF528A — ПОРОГ РАЗНЫЙ ДЛЯ РАЗНЫХ ЛИГ
#
# Решение Дмитрия: «в РПЛ нет дорогих трансферов, там они просто есть, можно
# от 2 миллионов». Общий порог в 15 млн отсекал русскую колонку начисто —
# самый дорогой переход окна, Карпукас в «Зенит» за 7 млн, до него не дотягивал
# вдвое, и на сайте не было ни одного российского трансфера.
#
# Опускать порог до двух для всех нельзя: из восьми лиг посыпались бы сотни
# проходных сделок, и сайт превратился бы в свалку — ровно то, чего мы
# избегаем штучной публикацией. Поэтому порог свой для России.
#
# Метка лиги берётся из страницы клуба (`league:` во front matter), обход её
# уже записывает — угадывать ничего не нужно.
LEAGUE_MIN_VALUE_M = {"РПЛ": 2.0}


def threshold_for(row: dict, default_m: float) -> float:
    return LEAGUE_MIN_VALUE_M.get(row.get("league") or "", default_m)


def seed(min_value_m: float) -> int:
    """Из результатов обхода делает записи в том же виде, что даёт разведка."""
    if not SCAN_FILE.exists():
        print("  сначала нужен --scan")
        return 0
    rows = json.loads(SCAN_FILE.read_text(encoding="utf-8"))
    todo = [r for r in rows
            if not r["on_site"]
            and r["value_eur"] >= threshold_for(r, min_value_m) * 1e6]
    print("  подходит под порог €%g млн (для РПЛ €%g): %d"
          % (min_value_m, LEAGUE_MIN_VALUE_M["РПЛ"], len(todo)))
    by_league: dict[str, int] = {}
    for row in todo:
        key = row.get("league") or "без лиги"
        by_league[key] = by_league.get(key, 0) + 1
    for key, count in sorted(by_league.items(), key=lambda x: -x[1]):
        print("     %-16s %d" % (key, count))

    with ThreadPoolExecutor(max_workers=6) as pool:
        prev = list(pool.map(
            lambda r: previous_club(r["tm_player_id"], r["tm_to_club_id"]), todo))

    ensure_dirs()
    made = 0
    for row, from_club in zip(todo, prev):
        if not from_club:
            print("  пропуск %s: прежний клуб не определён" % row["player_full_name"])
            continue
        # История стоимости иногда знает только текущий клуб — тогда
        # "прежний" совпадает с новым и переход превращается в бессмыслицу
        # вида "Ницца -> Ницца". Такие записи не заводим.
        if from_club.strip().lower() == row["to_club"].strip().lower():
            print("  пропуск %s: прежний клуб совпал с новым" % row["player_full_name"])
            continue
        surname = (row["player_full_name"].split() or [""])[-1]
        entity = "%s__%s__%s" % (slugify(surname), slugify(from_club), slugify(row["to_club"]))
        path = RECORDS_DIR / ("%s.json" % entity)
        if path.exists():
            continue
        path.write_text(json.dumps({
            "schema_version": 2,
            "kind": "official",
            "entity_id": entity,
            "player": surname,
            "player_full_name": row["player_full_name"],
            "from_club": from_club,
            "to_club": row["to_club"],
            "fee_raw": "",
            "verdict": "NEW_CANDIDATE",
            "pipeline_state": "DISCOVERED",
            "backfill": True,
            "source": {
                "publisher": "Transfermarkt",
                "tier": "reference",
                "url": "https://www.transfermarkt.com/-/profil/spieler/%s" % row["tm_player_id"],
                "title": "%s: переход в %s" % (row["player_full_name"], row["to_club"]),
                "published_iso": "%sT12:00:00+00:00" % row["start"],
            },
            "discovered_at": datetime.now(timezone.utc).isoformat(),
        }, ensure_ascii=False, indent=1), encoding="utf-8")
        made += 1
    print("  создано записей: %d" % made)
    return made


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Догон пропущенного окна")
    parser.add_argument("--scan", action="store_true")
    parser.add_argument("--seed", action="store_true")
    parser.add_argument("--from", dest="date_from", default="2026-08-20")
    parser.add_argument("--to", dest="date_to", default="2026-09-02")
    parser.add_argument("--min-value", type=float, default=15.0,
                        help="порог стоимости в млн евро")
    args = parser.parse_args(argv)

    if args.scan:
        rows = scan(args.date_from, args.date_to)
        miss = [r for r in rows if not r["on_site"]]
        print("\n  переходов в окне: %d | нет у нас: %d" % (len(rows), len(miss)))
        print("  файл: %s" % SCAN_FILE)
    if args.seed:
        seed(args.min_value)
    if not (args.scan or args.seed):
        parser.error("нужен --scan или --seed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
