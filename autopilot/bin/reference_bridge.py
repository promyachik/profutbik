"""
PROMYACHIK TRANSFER AUTOPILOT - REFERENCE BRIDGE

Строит справочники, которых не хватает между Transfermarkt и движком 3.4:

  1. country_map.json  - числовой countryId Transfermarkt -> страна, её русское
     название и код флага. Transfermarkt справочник стран наружу не отдаёт,
     поэтому таблица выводится из собственных данных сайта: берём страницы,
     где уже проставлено гражданство, и спрашиваем у TM nationalityId тех же
     игроков по их player_id.

  2. club_bridge.json  - TM club id -> API-Football club id. Движку 3.4 для
     логотипов нужен именно API-Football id.

  3. POSITIONS         - позиция Transfermarkt -> русское название в принятом
     на сайте написании.

Неизвестное значение НИКОГДА не угадывается: оно остаётся пустым, и кандидат
уходит в NEEDS_REVIEW.

Ничего не публикует и не изменяет Promyachik_CLEAN.
"""
from __future__ import annotations

import argparse
import json
import re
import ssl
import sys
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from transfer_discovery import ACTIVE_PROJECT, PARSER_ROOT, normalize  # noqa: E402
from transfer_enrichment import (  # noqa: E402
    TM_API, CACHE_DIR, build_tm_club_index, club_tokens,
)

COUNTRY_MAP_PATH = CACHE_DIR / "country_map.json"
CLUB_BRIDGE_PATH = CACHE_DIR / "club_bridge.json"

# Трёхбуквенные коды ФИФА. Из ISO-2 механически не выводятся
# (Germany -> GER, а не DEU), поэтому таблица задана явно.
# Страны вне таблицы кандидат не публикуют: он уходит в NEEDS_REVIEW.
FIFA_CODES = {
    "Argentina": "ARG", "Belgium": "BEL", "Bosnia-Herzegovina": "BIH",
    "Brazil": "BRA", "Cameroon": "CMR", "Cote d'Ivoire": "CIV",
    "Croatia": "CRO", "Ecuador": "ECU", "Egypt": "EGY", "England": "ENG",
    "France": "FRA", "Germany": "GER", "Greece": "GRE", "Italy": "ITA",
    "Northern Ireland": "NIR", "Paraguay": "PAR", "Poland": "POL",
    "Portugal": "POR", "Senegal": "SEN", "Spain": "ESP",
    "Switzerland": "SUI", "Ukraine": "UKR", "Uruguay": "URU", "Wales": "WAL",
    # Часто встречающиеся сверх текущей выборки сайта.
    "Netherlands": "NED", "Scotland": "SCO", "Ireland": "IRL",
    "Denmark": "DEN", "Sweden": "SWE", "Norway": "NOR", "Austria": "AUT",
    "Turkey": "TUR", "Serbia": "SRB", "Russia": "RUS", "Colombia": "COL",
    "Chile": "CHI", "Mexico": "MEX", "United States": "USA", "Canada": "CAN",
    "Japan": "JPN", "Korea, South": "KOR", "Australia": "AUS",
    "Nigeria": "NGA", "Ghana": "GHA", "Morocco": "MAR", "Algeria": "ALG",
    "Tunisia": "TUN", "Mali": "MLI", "Guinea": "GUI", "Congo": "CGO",
    "DR Congo": "COD", "Albania": "ALB", "Czech Republic": "CZE",
    "Slovakia": "SVK", "Slovenia": "SVN", "Hungary": "HUN", "Romania": "ROU",
    "Bulgaria": "BUL", "Finland": "FIN", "Iceland": "ISL", "Georgia": "GEO",
    "Armenia": "ARM", "Israel": "ISR", "Uzbekistan": "UZB", "Iran": "IRN",
    "Saudi Arabia": "KSA", "Qatar": "QAT", "Venezuela": "VEN", "Peru": "PER",
    "Bolivia": "BOL", "Costa Rica": "CRC", "Panama": "PAN", "Jamaica": "JAM",
}

# Позиции Transfermarkt в написании, принятом на сайте.
POSITIONS = {
    "Goalkeeper": ("Вратарь", "GK"),
    "Centre-Back": ("Центральный защитник", "CB"),
    "Left-Back": ("Левый защитник", "LB"),
    "Right-Back": ("Правый защитник", "RB"),
    "Defensive Midfield": ("Опорный полузащитник", "DM"),
    "Central Midfield": ("Центральный полузащитник", "CM"),
    "Attacking Midfield": ("Атакующий полузащитник", "AM"),
    "Left Midfield": ("Левый полузащитник", "LM"),
    "Right Midfield": ("Правый полузащитник", "RM"),
    "Left Winger": ("Левый вингер", "LW"),
    "Right Winger": ("Правый вингер", "RW"),
    "Second Striker": ("Оттянутый нападающий", "SS"),
    "Centre-Forward": ("Центральный нападающий", "CF"),
}


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def api(path: str) -> dict:
    request = urllib.request.Request(TM_API + path, headers={
        "User-Agent": "Mozilla/5.0", "Accept": "application/json"})
    with urllib.request.urlopen(
            request, timeout=25, context=ssl.create_default_context()) as response:
        return json.loads(response.read())


# ---------------------------------------------------------------------------
# 1. Справочник стран
# ---------------------------------------------------------------------------

def site_nationalities() -> list[dict]:
    """Страницы сайта, где есть и TM ID, и проставленное гражданство."""
    rows = []
    root = ACTIVE_PROJECT / "content" / "transfers"
    for directory in sorted(root.iterdir()):
        page = directory / "index.md"
        if not page.is_file():
            continue
        text = page.read_text(encoding="utf-8", errors="replace")
        parts = text.split("---")
        if len(parts) < 3:
            continue
        front = parts[1]

        def field(key: str) -> str:
            match = re.search(r'(?m)^%s:\s*"?([^"\n]+?)"?\s*$' % key, front)
            return match.group(1).strip() if match else ""

        tm_id = field("transfermarkt_player_id")
        name_en = field("nationality")
        name_ru = field("nationality_ru") or field("nationality_name")
        flag = field("nationality_flag")
        flag_code = ""
        if flag:
            flag_code = Path(flag).stem.lower()
        if tm_id and name_en and name_ru and flag_code:
            rows.append({"tm_player_id": tm_id, "name": name_en,
                         "name_ru": name_ru, "flag_code": flag_code})
    return rows


def build_country_map(verbose: bool = True) -> dict:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    rows = site_nationalities()
    if verbose:
        print("  страниц с TM ID и гражданством: %d" % len(rows))

    def nationality_id(row: dict) -> tuple[dict, int | None]:
        try:
            data = api("/player/%s" % row["tm_player_id"])["data"]
            value = (data.get("nationalityDetails") or {}).get("nationalities") or {}
            return row, value.get("nationalityId")
        except Exception:
            return row, None

    country_map: dict[str, dict] = {}
    conflicts: list[str] = []
    with ThreadPoolExecutor(max_workers=6) as pool:
        for row, country_id in pool.map(nationality_id, rows):
            if not country_id:
                continue
            key = str(country_id)
            entry = {"name": row["name"], "name_ru": row["name_ru"],
                     "flag_code": row["flag_code"],
                     "fifa_code": FIFA_CODES.get(row["name"], "")}
            existing = country_map.get(key)
            if existing and existing != entry:
                # Русское/английское написание на сайте местами расходится.
                # Предпочитаем латинское название страны.
                if not re.match(r"^[A-Za-z]", existing["name"]):
                    country_map[key] = entry
                conflicts.append("%s: %r против %r" % (
                    key, existing["name"], entry["name"]))
                continue
            country_map[key] = entry

    payload = {"built_at": now_iso(), "source": "site pages + TM player API",
               "countries": country_map}
    COUNTRY_MAP_PATH.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    if verbose:
        print("  стран в справочнике: %d" % len(country_map))
        if conflicts:
            print("  расхождения написания (взято латинское): %d" % len(conflicts))
    return country_map


# ---------------------------------------------------------------------------
# 2. Мост TM club -> API-Football club
# ---------------------------------------------------------------------------

def api_football_clubs() -> dict[str, str]:
    """normalized name -> API-Football id (из локального каталога логотипов)."""
    data = json.loads(
        (ACTIVE_PROJECT / "data" / "club-logos.json").read_text(encoding="utf-8"))
    clubs = data.get("clubs", data)
    result: dict[str, str] = {}
    if isinstance(clubs, dict):
        for club_id, entry in clubs.items():
            name = str((entry or {}).get("name") or "").strip()
            if name:
                result[normalize(name)] = str(club_id)
    return result


def build_club_bridge(verbose: bool = True) -> dict:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    tm_clubs = build_tm_club_index(verbose=False)          # name -> tm id
    api_clubs = api_football_clubs()                        # name -> api id

    bridge: dict[str, dict] = {}
    unmatched: list[str] = []

    for tm_name, tm_id in tm_clubs.items():
        api_id = api_clubs.get(tm_name)
        matched_name = tm_name
        if not api_id:
            wanted = club_tokens(tm_name)
            candidates = []
            for api_name, value in api_clubs.items():
                have = club_tokens(api_name)
                if have and (wanted <= have or have <= wanted):
                    candidates.append((len(have ^ wanted), api_name, value))
            candidates.sort()
            if candidates:
                best = [c for c in candidates if c[0] == candidates[0][0]]
                if len(best) == 1:
                    api_id, matched_name = best[0][2], best[0][1]
        if api_id:
            bridge[tm_id] = {"tm_name": tm_name, "api_football_id": int(api_id),
                             "api_name": matched_name}
        else:
            unmatched.append(tm_name)

    payload = {"built_at": now_iso(), "bridge": bridge,
               "unmatched_tm_clubs": sorted(unmatched)}
    CLUB_BRIDGE_PATH.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    if verbose:
        print("  клубов TM всего            : %d" % len(tm_clubs))
        print("  связано с API-Football     : %d" % len(bridge))
        print("  без связи (нужен lookup)   : %d" % len(unmatched))
    return payload


# ---------------------------------------------------------------------------

def load_country_map() -> dict:
    if COUNTRY_MAP_PATH.exists():
        return json.loads(COUNTRY_MAP_PATH.read_text(encoding="utf-8"))["countries"]
    return {}


def load_club_bridge() -> dict:
    if CLUB_BRIDGE_PATH.exists():
        return json.loads(CLUB_BRIDGE_PATH.read_text(encoding="utf-8"))["bridge"]
    return {}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Promyachik reference bridge builder")
    parser.add_argument("--countries", action="store_true")
    parser.add_argument("--clubs", action="store_true")
    args = parser.parse_args(argv)
    do_all = not (args.countries or args.clubs)

    if args.countries or do_all:
        print("\n=== СПРАВОЧНИК СТРАН ===")
        countries = build_country_map()
        for key in sorted(countries, key=lambda k: countries[k]["name"]):
            entry = countries[key]
            print("  %-5s %-22s %-24s %s" % (
                key, entry["name"], entry["name_ru"], entry["flag_code"]))

    if args.clubs or do_all:
        print("\n=== МОСТ TM -> API-FOOTBALL ===")
        payload = build_club_bridge()
        unmatched = payload["unmatched_tm_clubs"]
        if unmatched:
            print("  примеры без связи: %s" % ", ".join(unmatched[:8]))

    print("\n=== ПОЗИЦИИ: %d ===" % len(POSITIONS))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
