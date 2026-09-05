"""
PROMYACHIK — ГЕНЕРАТОР КЛУБНЫХ СТРАНИЦ

Собирает страницу клуба из данных, которые парсер и так загружает:
состав с возрастом и рыночной стоимостью, показатели команды и все
трансферы этого клуба, уже опубликованные на сайте.

Ничего не выдумывает: нет данных - блок не выводится.

    python club_pages.py --club "Newcastle" --save
    python club_pages.py --all --save        (все клубы справочника)
"""
from __future__ import annotations

import argparse
import hashlib
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
from transfer_discovery import ACTIVE_PROJECT, normalize, slugify  # noqa: E402
from transfer_enrichment import (  # noqa: E402
    api, build_tm_club_index, club_tokens, resolve_tm_club, squad_players,
)
from reference_bridge import POSITIONS, load_club_bridge  # noqa: E402
from job_builder import (  # noqa: E402
    ApiFootballQuotaExceeded, api_football_lookup, club_word,
    compact_money, plural_ru,
)

CLUBS_DIR = ACTIVE_PROJECT / "content" / "clubs"
CLUB_LOGOS = ACTIVE_PROJECT / "data" / "club-logos.json"
TRANSFERS_JSON = ACTIVE_PROJECT / "data" / "transfers.json"

# Догрузка логотипа отсутствующего клуба включается флагом --network.
ALLOW_NETWORK = False

# Страна турнира — подсказка для API-Football. Без неё "Newcastle"
# неоднозначен: он есть и в Англии, и в Северной Ирландии.
# ID лиг API-Football — под тот же селектор, что уже есть в разделе слухов.
COMPETITION_LEAGUE_ID = {
    "GB1": "39", "ES1": "140", "IT1": "135", "L1": "78", "FR1": "61",
    "TR1": "203", "PO1": "94", "RU1": "235", "NL1": "88", "BE1": "144",
    "SA1": "307", "GB2": "40",
}

COMPETITION_COUNTRY = {
    "GB1": "England", "GB2": "England", "ES1": "Spain", "IT1": "Italy",
    "L1": "Germany", "FR1": "France", "RU1": "Russia", "PO1": "Portugal",
    "NL1": "Netherlands", "TR1": "Turkey", "BE1": "Belgium",
    "SA1": "Saudi-Arabia",
}

LEAGUE_RU = {
    "GB1": "Премьер-лига", "ES1": "Ла Лига", "IT1": "Серия А",
    "L1": "Бундеслига", "FR1": "Лига 1", "RU1": "РПЛ",
    "SA1": "Про-лига Саудовской Аравии", "PO1": "Примейра",
    "NL1": "Эредивизи", "TR1": "Суперлига", "BE1": "Про-лига",
    "GB2": "Чемпионшип",
}


def money(value: float) -> str:
    if value >= 1_000_000_000:
        return "€%s млрд" % ("%.2f" % (value / 1e9)).replace(".", ",")
    if value >= 1_000_000:
        return "€%s млн" % ("%g" % round(value / 1e6, 1)).replace(".", ",")
    return "€%s тыс." % ("%g" % round(value / 1e3)).replace(".", ",")


def club_catalog() -> dict:
    data = json.loads(CLUB_LOGOS.read_text(encoding="utf-8"))
    return data.get("clubs", data)


def same_club(left: str, right: str) -> bool:
    """Transfermarkt и наши данные зовут клубы по-разному:
    "Newcastle United" против "Newcastle". Сравниваем по значимым словам."""
    if not left or not right:
        return False
    if normalize(left) == normalize(right):
        return True
    a, b = club_tokens(left), club_tokens(right)
    return bool(a) and bool(b) and (a <= b or b <= a)


def api_logo(club_name: str) -> tuple[str, str, str]:
    """(путь логотипа, код, страна) из локального каталога.

    Сначала точное совпадение названия, и только потом — по значимым словам.
    Если под запрос подходит несколько разных клубов, возвращается пусто:
    подставить чужую эмблему хуже, чем не подставить никакой.
    """
    exact, loose = [], []
    for entry in club_catalog().values():
        names = [entry.get("name") or "", entry.get("configured_name") or ""]
        if any(normalize(n) == normalize(club_name) for n in names if n):
            exact.append(entry)
        elif any(same_club(n, club_name) for n in names if n):
            loose.append(entry)

    chosen = None
    if len(exact) >= 1:
        chosen = exact[0]
    elif len(loose) == 1:
        chosen = loose[0]

    if not chosen:
        return "", "", ""
    return (chosen.get("logo") or "", chosen.get("code") or "",
            chosen.get("country") or "")


from paths import ENGINE as ENGINE_PATH  # noqa: E402


def load_engine():
    """Замороженный движок 3.4 — в нём уже есть загрузка и кэш логотипов."""
    import importlib.util
    spec = importlib.util.spec_from_file_location("pf_engine_clubs", ENGINE_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def fetch_missing_logo(club_name: str, country: str = "") -> tuple[str, str, str]:
    """Клуба нет в локальном каталоге: точный lookup и загрузка одного клуба.

    Политика проекта - on-demand: качаем только нужный клуб, не лигу целиком.
    Неоднозначный результат - ничего не качаем.
    """
    try:
        api_id = api_football_lookup(club_name, country)
    except ApiFootballQuotaExceeded as error:
        print("     ЛИМИТ API-Football: %s" % error)
        print("     логотип не получен по квоте, а не потому что клуба нет")
        return "", "", ""
    if not api_id:
        return "", "", ""
    try:
        engine = load_engine()
        engine.verify_club_logo(ACTIVE_PROJECT, int(api_id), club_name)
    except Exception as error:
        print("     логотип не получен: %s" % str(error)[:70])
        return "", "", ""
    return api_logo(club_name)


# PF503A. Запасной источник эмблемы — герб Transfermarkt по id клуба.
#
# API-Football ищется по названию, и на 13 клубах из 148 поиск не давал
# однозначного ответа: он зовёт их короче нашего ("Malaga" против "Málaga CF",
# "Sassuolo" против "US Sassuolo"), а у "Rodina Moscow" записи нет вовсе.
# Страницы выходили с пустым местом под логотип.
#
# Здесь имя не участвует: id клуба на Transfermarkt мы уже знаем — по нему
# только что загружен состав. Промаха быть не может по построению.
TM_CREST_URL = "https://tmssl.akamaized.net/images/wappen/homepageWappen150x150/%s.png"
TM_LOGO_DIR = Path("images") / "clubs" / "tm" / "rendered"


def existing_api_id(club_name: str) -> str:
    """id API-Football, уже записанный на странице этого клуба.

    У клубов с гербом Transfermarkt id взять неоткуда: в каталоге логотипов
    их нет, а из пути к гербу читается id Transfermarkt, не API-Football.
    Он проставлен вручную (PF505A) и должен пережить перегенерацию.
    """
    page = CLUBS_DIR / slugify(club_name) / "index.md"
    if not page.is_file():
        return ""
    found = re.search(r'(?m)^api_football_id:\s*"(\d*)"',
                      page.read_text(encoding="utf-8", errors="replace"))
    return found.group(1) if found else ""


def existing_logo(club_name: str) -> str:
    """Эмблема, уже стоящая на странице этого клуба.

    Каталог логотипов заполняется только из API-Football, поэтому герб TM
    в нём не окажется никогда. Без этой проверки перегенерация лиги без
    --network затирала бы уже поставленный герб пустой строкой.
    """
    page = CLUBS_DIR / slugify(club_name) / "index.md"
    if not page.is_file():
        return ""
    found = re.search(r'(?m)^club_logo:\s*"([^"]*)"',
                      page.read_text(encoding="utf-8", errors="replace"))
    value = found.group(1) if found else ""
    if value and (ACTIVE_PROJECT / "static" / value).is_file():
        return value
    return ""


def fetch_tm_crest(tm_id: str, club_name: str = "") -> str:
    """Герб с Transfermarkt в static, путь для front matter. Пусто при неудаче."""
    if not str(tm_id).strip().isdigit():
        return ""
    try:
        request = urllib.request.Request(
            TM_CREST_URL % tm_id, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(
                request, timeout=25, context=ssl.create_default_context()) as response:
            raw = response.read()
    except Exception as error:
        print("     герб Transfermarkt не получен: %s" % str(error)[:70])
        return ""

    # Проверяем то же, что движок проверяет у логотипов API-Football: это
    # действительно PNG разумного размера, а не заглушка и не страница ошибки.
    if raw[:8] != b"\x89PNG\r\n\x1a\n" or len(raw) < 2048:
        print("     герб Transfermarkt отбракован: не PNG или слишком мал")
        return ""
    width, height = struct.unpack(">II", raw[16:24])
    if width < 100 or height < 100:
        print("     герб Transfermarkt отбракован: %dx%d" % (width, height))
        return ""

    digest = hashlib.sha256(raw).hexdigest()
    relative = (TM_LOGO_DIR / ("%s-%s.png" % (tm_id, digest[:12]))).as_posix()
    target = ACTIVE_PROJECT / "static" / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(raw)
    print("     герб Transfermarkt: %s (%dx%d)" % (relative, width, height))
    return relative


def site_transfers(club_name: str) -> list[dict]:
    """Трансферы этого клуба, уже опубликованные у нас."""
    rows = json.loads(TRANSFERS_JSON.read_text(encoding="utf-8"))
    found = []
    for row in rows:
        if not isinstance(row, dict) or not row.get("slug"):
            continue
        to_name = row.get("to_club_name") or row.get("to_name") or ""
        from_name = row.get("from_club_name") or row.get("from_name") or ""
        if same_club(club_name, to_name):
            found.append({"direction": "in", "row": row})
        elif same_club(club_name, from_name):
            found.append({"direction": "out", "row": row})
    return found


def build_club(club_name: str, tm_clubs: dict) -> dict | None:
    club_id = resolve_tm_club(club_name, tm_clubs)
    if not club_id:
        return None
    club = api("/club/%s" % club_id)["data"]
    base = club.get("baseDetails") or {}
    details = club.get("squadDetails") or {}
    superior = base.get("superiorClub") or {}
    players = squad_players(club_id)

    def value_of(person: dict) -> float:
        current = ((person.get("marketValueDetails") or {}).get("current") or {})
        return float(current.get("value") or 0)

    squad = []
    for person in sorted(players, key=value_of, reverse=True):
        attributes = person.get("attributes") or {}
        position_en = (attributes.get("position") or {}).get("name") or ""
        squad.append({
            "name": person.get("name") or "",
            "tm_id": str(person.get("id") or ""),
            "position_ru": POSITIONS.get(position_en, ("", ""))[0] or position_en,
            "position_short": (attributes.get("position") or {}).get("shortName") or "",
            "age": (person.get("lifeDates") or {}).get("age"),
            "value": value_of(person),
            "value_display": money(value_of(person)) if value_of(person) else "",
        })

    resolved_name = club.get("name") or club_name
    competition = base.get("primaryCompetitionId") or ""
    logo, code, country = api_logo(resolved_name)
    if not logo:
        logo = existing_logo(resolved_name)
        if logo:
            print("     эмблема уже стоит на странице: %s" % logo)
    if not logo and ALLOW_NETWORK:
        print("     логотипа нет в каталоге, пробую загрузить...")
        logo, code, country = fetch_missing_logo(
            resolved_name, COMPETITION_COUNTRY.get(competition, ""))
        if logo:
            print("     логотип получен: %s" % logo)
        else:
            print("     в API-Football клуб не опознан однозначно, беру герб TM")
            logo = fetch_tm_crest(club_id, resolved_name)
    # Когда логотип пришёл из API-Football, id зашит в его путь и сомнений
    # не вызывает. Для гербов Transfermarkt берём то, что уже на странице.
    found = re.search(r"/api/(?:rendered/)?(\d+)", logo)
    api_id = found.group(1) if found else existing_api_id(resolved_name)

    return {
        "name": club.get("name") or club_name,
        "tm_id": club_id,
        "api_id": api_id,
        "code": code,
        "country": country,
        "competition": competition,
        "league_ru": LEAGUE_RU.get(competition, ""),
        "league_id": COMPETITION_LEAGUE_ID.get(competition, ""),
        "logo": logo,
        "city": (superior.get("location") or {}).get("city") or "",
        "squad_size": len(squad),
        "average_age": str(details.get("averageAgeDisplay") or "").replace(".", ","),
        "squad_value": compact_money(
            (details.get("currentMarketValue") or {}).get("compact") or {}),
        # Строку "€1,03 млрд" Hugo сортирует лексически и ставит её раньше
        # "€252,90 млн". Для сортировки нужно число.
        "squad_value_eur": int((details.get("currentMarketValue") or {}).get("value") or 0),
        "average_value": compact_money(
            (details.get("averageMarketValue") or {}).get("compact") or {}),
        "squad": squad,
        "transfers": site_transfers(club.get("name") or club_name),
    }


def render_page(club: dict) -> str:
    slug = slugify(club["name"])
    title = "%s: состав, стоимость и трансферы" % club["name"]
    description = "Состав %s — %d %s, средний возраст %s." % (
        club_word(club["name"], "gen"), club["squad_size"],
        plural_ru(club["squad_size"], "игрок", "игрока", "игроков"),
        club["average_age"] or "не указан")
    if club["squad_value"]:
        description += " Общая стоимость команды %s." % club["squad_value"]

    front = [
        "---",
        'title: "%s"' % title,
        'description: "%s"' % description,
        'date: "%s"' % datetime.now().astimezone().isoformat(timespec="seconds"),
        'url: "/clubs/%s/"' % slug,
        "draft: false",
        'type: "clubs"',
        'layout: "single"',
        'club_name: "%s"' % club["name"],
        'club_code: "%s"' % club["code"],
        'club_logo: "%s"' % club["logo"],
        'api_football_id: "%s"' % club["api_id"],
        'club_city: "%s"' % club["city"],
        'club_country: "%s"' % club["country"],
        'league: "%s"' % club["league_ru"],
        'league_id: "%s"' % club["league_id"],
        'transfermarkt_club_id: "%s"' % club["tm_id"],
        "squad_size: %d" % club["squad_size"],
        'average_age: "%s"' % club["average_age"],
        'squad_value: "%s"' % club["squad_value"],
        "squad_value_eur: %d" % club["squad_value_eur"],
        'average_value: "%s"' % club["average_value"],
        "squad:",
    ]
    for person in club["squad"]:
        front += [
            "  - name: %s" % json.dumps(person["name"], ensure_ascii=False),
            "    position: %s" % json.dumps(person["position_ru"], ensure_ascii=False),
            "    position_short: %s" % json.dumps(person["position_short"],
                                                  ensure_ascii=False),
            "    age: %s" % (person["age"] if person["age"] else '""'),
            "    value: %s" % json.dumps(person["value_display"], ensure_ascii=False),
            "    tm_id: %s" % json.dumps(person["tm_id"], ensure_ascii=False),
        ]

    front.append("club_transfers:")
    for item in club["transfers"]:
        row = item["row"]
        other = (row.get("from_club_name") or row.get("from_name") or ""
                 ) if item["direction"] == "in" else (
                 row.get("to_club_name") or row.get("to_name") or "")
        front += [
            "  - player: %s" % json.dumps(
                row.get("player") or row.get("player_name") or "", ensure_ascii=False),
            "    slug: %s" % json.dumps(row.get("slug") or "", ensure_ascii=False),
            "    direction: %s" % json.dumps(item["direction"]),
            "    other_club: %s" % json.dumps(other, ensure_ascii=False),
            "    fee: %s" % json.dumps(row.get("fee") or "", ensure_ascii=False),
        ]
    front.append("---")
    front.append("")

    top = club["squad"][0] if club["squad"] else None
    body = []
    lead = "В заявке %s — %d %s" % (
        club_word(club["name"], "gen"), club["squad_size"],
        plural_ru(club["squad_size"], "игрок", "игрока", "игроков"))
    if club["average_age"]:
        lead += " со средним возрастом %s года" % club["average_age"]
    lead += "."
    if club["squad_value"]:
        lead += " Общая стоимость команды по оценке Transfermarkt — %s" % club["squad_value"]
        if club["average_value"]:
            lead += ", в среднем %s на игрока" % club["average_value"]
        lead += "."
    body.append(lead)

    if top and top["value_display"]:
        body.append("Самый дорогой игрок состава — %s (%s), его стоимость оценивается "
                    "в %s." % (top["name"], top["position_ru"].lower(),
                               top["value_display"]))

    incoming = [t for t in club["transfers"] if t["direction"] == "in"]
    outgoing = [t for t in club["transfers"] if t["direction"] == "out"]
    if incoming or outgoing:
        parts = []
        if incoming:
            parts.append("пришли %d" % len(incoming))
        if outgoing:
            parts.append("ушли %d" % len(outgoing))
        body.append("Трансферы клуба, о которых мы писали: %s." % ", ".join(parts))

    return "\n".join(front) + "\n\n".join(body) + "\n"


def competition_clubs(code: str) -> list[str]:
    """Названия клубов турнира по таблице Transfermarkt."""
    table = api("/competition/%s/table" % code)["data"]
    names = []
    for row in table["tables"][0]["clubs"]:
        try:
            names.append(api("/club/%s" % row["clubId"])["data"]["name"])
        except Exception:
            continue
    return names


def rebuild_club_links() -> int:
    """data/club_links.json — карта «id API-Football -> адрес страницы клуба».

    Нужна для перелинковки: в статье о трансфере клуб зовётся "Barcelona",
    а страница — "FC Barcelona". Связывать по названию ненадёжно, по id точно.
    Отдельный файл данных, а не запрос к страницам: обращение к site.Pages
    во время их же рендеринга вешает сборку Hugo.
    """
    import re as _re
    links = {}
    if not CLUBS_DIR.exists():
        return 0
    for directory in sorted(CLUBS_DIR.iterdir()):
        page = directory / "index.md"
        if not page.is_file():
            continue
        text = page.read_text(encoding="utf-8", errors="replace")
        url = _re.search(r'(?m)^url:\s*"([^"]*)"', text)
        name = _re.search(r'(?m)^club_name:\s*"([^"]*)"', text)
        if not url:
            continue

        # Сначала явное поле: у клубов с гербом Transfermarkt в пути к
        # картинке лежит id Transfermarkt, и разбор пути дал бы чужой номер.
        # Разбор оставлен запасным — на страницах старых прогонов поля нет.
        club_id = _re.search(r'(?m)^api_football_id:\s*"(\d+)"', text)
        if club_id:
            club_id = club_id.group(1)
        else:
            logo = _re.search(r'(?m)^club_logo:\s*"([^"]*)"', text)
            found = _re.search(r"/api/(?:rendered/)?(\d+)", logo.group(1)) if logo else None
            if not found:
                continue
            club_id = found.group(1)

        links[club_id] = {
            "url": url.group(1),
            "name": name.group(1) if name else directory.name,
        }
    out = ACTIVE_PROJECT / "data" / "club_links.json"
    out.write_text(json.dumps(links, ensure_ascii=False, indent=2) + "\n",
                   encoding="utf-8")
    return len(links)


def fix_missing_logos() -> int:
    """Дозаполнить эмблемы на уже существующих страницах, не трогая остальное.

    Перегенерировать лигу ради одной картинки дорого: это тысячи запросов
    к Transfermarkt за составами. Здесь правится только строка club_logo.
    """
    fixed = 0
    for directory in sorted(CLUBS_DIR.iterdir()):
        page = directory / "index.md"
        if not page.is_file():
            continue
        text = page.read_text(encoding="utf-8", errors="replace")
        logo = re.search(r'(?m)^club_logo:\s*"([^"]*)"', text)
        if logo and logo.group(1).strip():
            continue
        tm_id = re.search(r'(?m)^transfermarkt_club_id:\s*"(\d+)"', text)
        name = re.search(r'(?m)^club_name:\s*"([^"]*)"', text)
        if not tm_id:
            print("  %s: нет id Transfermarkt, пропуск" % directory.name)
            continue
        print("  %s" % (name.group(1) if name else directory.name))
        relative = fetch_tm_crest(tm_id.group(1), name.group(1) if name else "")
        if not relative:
            continue
        page.write_text(
            re.sub(r'(?m)^club_logo:\s*""\s*$', 'club_logo: "%s"' % relative,
                   text, count=1),
            encoding="utf-8")
        fixed += 1
    print("\n  эмблем добавлено: %d" % fixed)
    return fixed


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Promyachik club page generator")
    parser.add_argument("--club", help="название клуба")
    parser.add_argument("--all", action="store_true", help="все клубы справочника")
    parser.add_argument("--competition", help="код турнира: GB1, ES1, IT1, L1, FR1, RU1 ...")
    parser.add_argument("--save", action="store_true")
    parser.add_argument("--network", action="store_true",
                        help="догружать логотипы клубов, которых нет в каталоге")
    parser.add_argument("--fix-logos", action="store_true",
                        help="дозаполнить пустые эмблемы гербами Transfermarkt")
    args = parser.parse_args(argv)

    global ALLOW_NETWORK
    ALLOW_NETWORK = args.network

    if args.fix_logos:
        if fix_missing_logos():
            print("  карта перелинковки: %d клубов\n" % rebuild_club_links())
        return 0

    tm_clubs = build_tm_club_index(verbose=False)
    names = []
    if args.club:
        names = [args.club]
    elif args.competition:
        names = competition_clubs(args.competition)
        print("  клубов в турнире %s: %d" % (args.competition, len(names)))
    elif args.all:
        names = sorted({entry.get("name") for entry in club_catalog().values()
                        if entry.get("name")})
    else:
        parser.error("нужен --club, --competition или --all")

    made = 0
    for name in names:
        club = build_club(name, tm_clubs)
        if not club:
            print("  пропуск: %s — клуб не опознан" % name)
            continue
        print("\n  %s (TM %s)" % (club["name"], club["tm_id"]))
        print("     %s · %s · %s" % (club["league_ru"] or "?", club["city"] or "?",
                                     club["squad_value"] or "?"))
        print("     состав: %d | трансферов на сайте: %d"
              % (club["squad_size"], len(club["transfers"])))
        if args.save:
            slug = slugify(club["name"])
            directory = CLUBS_DIR / slug
            directory.mkdir(parents=True, exist_ok=True)
            (directory / "index.md").write_text(render_page(club), encoding="utf-8")
            print("     -> content/clubs/%s/index.md" % slug)
            made += 1
    if args.save:
        print("\n  создано страниц: %d" % made)
        print("  карта перелинковки: %d клубов\n" % rebuild_club_links())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
