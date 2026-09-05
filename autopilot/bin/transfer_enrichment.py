"""
PROMYACHIK TRANSFER AUTOPILOT - ENRICHMENT (read-only)

Берёт кандидатов, найденных разведкой, и доводит их до однозначной
идентичности через Transfermarkt.

Ключевая идея подтверждения:
    состоявшийся переход означает, что игрок УЖЕ числится в составе
    клуба назначения на Transfermarkt.

Поэтому поиск игрока в составе клуба назначения выполняет сразу две задачи:
опознаёт игрока (даёт точный player_id и полное имя) и подтверждает сам факт
перехода. Если игрока в составе нет - это не подтверждённый переход,
и кандидат уходит в NEEDS_REVIEW, а не публикуется.

Ничего не публикует и не изменяет Promyachik_CLEAN.
"""
from __future__ import annotations

import argparse
import json
import re
import ssl
import sys
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from transfer_discovery import (  # noqa: E402
    ACTIVE_PROJECT, PARSER_ROOT, RECORDS_DIR,
    build_club_index, normalize, slugify, surname,
)

TM_API = "https://tmapi-alpha.transfermarkt.technology"
CACHE_DIR = PARSER_ROOT / "state" / "cache"
CLUB_INDEX_PATH = CACHE_DIR / "tm_clubs.json"
CLUB_INDEX_TTL_DAYS = 7

# Соревнования, которые покрываем. Неизвестные коды просто пропускаются.
COMPETITIONS = [
    ("GB1", "Premier League"), ("ES1", "La Liga"), ("IT1", "Serie A"),
    ("L1", "Bundesliga"), ("FR1", "Ligue 1"), ("RU1", "Premier Liga"),
    ("SA1", "Saudi Pro League"), ("PO1", "Primeira Liga"),
    ("NL1", "Eredivisie"), ("TR1", "Super Lig"), ("BE1", "Pro League"),
    ("GB2", "Championship"),
]

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36"
)


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def api(path: str) -> dict:
    request = urllib.request.Request(TM_API + path, headers={
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json",
    })
    with urllib.request.urlopen(
            request, timeout=25, context=ssl.create_default_context()) as response:
        return json.loads(response.read())


# ---------------------------------------------------------------------------
# Справочник клубов Transfermarkt (кэшируется на диск)
# ---------------------------------------------------------------------------

def build_tm_club_index(refresh: bool = False, verbose: bool = True) -> dict[str, str]:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)

    if CLUB_INDEX_PATH.exists() and not refresh:
        cached = json.loads(CLUB_INDEX_PATH.read_text(encoding="utf-8"))
        age_days = (time.time() - cached.get("built_at_epoch", 0)) / 86400
        if age_days < CLUB_INDEX_TTL_DAYS:
            if verbose:
                print("  справочник клубов TM: из кэша, %d клубов, возраст %.1f дн."
                      % (len(cached["clubs"]), age_days))
            return cached["clubs"]

    if verbose:
        print("  строю справочник клубов Transfermarkt...")
    club_ids: set[str] = set()
    for code, title in COMPETITIONS:
        try:
            table = api("/competition/%s/table" % code)["data"]
            ids = [row["clubId"] for row in table["tables"][0]["clubs"]]
            club_ids.update(ids)
            if verbose:
                print("    %-4s %-18s %d клубов" % (code, title, len(ids)))
        except Exception as error:
            if verbose:
                print("    %-4s %-18s пропущено: %s" % (code, title, str(error)[:40]))

    def club_name(club_id: str) -> tuple[str, str]:
        try:
            return club_id, api("/club/%s" % club_id)["data"]["name"]
        except Exception:
            return club_id, ""

    clubs: dict[str, str] = {}
    with ThreadPoolExecutor(max_workers=6) as pool:
        for club_id, name in pool.map(club_name, sorted(club_ids)):
            if name:
                clubs[normalize(name)] = club_id

    CLUB_INDEX_PATH.write_text(json.dumps({
        "built_at": now_iso(),
        "built_at_epoch": time.time(),
        "clubs": clubs,
    }, ensure_ascii=False, indent=2), encoding="utf-8")
    if verbose:
        print("  справочник клубов TM: собрано %d клубов" % len(clubs))
    return clubs


# Слова, которые ничего не значат при сопоставлении названий клубов.
# Только формальные приставки и суффиксы. Слова, различающие клубы,
# сюда попадать НЕ должны: "united" и "city" здесь сводили Manchester City
# и Manchester United к одному {manchester}, и клубы путались.
CLUB_STOPWORDS = {
    "fc", "cf", "sc", "ac", "afc", "cfc", "ssc", "as", "rc", "sv", "vfb", "vfl",
    "tsg", "bsc", "fk", "sk", "club", "de", "futbol", "football", "calcio", "and",
}


def club_tokens(value: str) -> frozenset[str]:
    tokens = [t for t in normalize(value).split() if t not in CLUB_STOPWORDS]
    return frozenset(tokens or normalize(value).split())


def resolve_tm_club(name: str, tm_clubs: dict[str, str]) -> str | None:
    """TM club id по названию.

    Порядок: точное совпадение -> совпадение по значимым словам.
    Если под запрос подходит несколько разных клубов (например "Real" -
    Madrid, Sociedad, Betis), возвращается None. Угадывать нельзя.
    """
    key = normalize(name)
    if not key:
        return None
    if key in tm_clubs:
        return tm_clubs[key]

    wanted = club_tokens(name)
    if not wanted:
        return None

    matches: list[tuple[int, str, str]] = []
    for candidate_key, club_id in tm_clubs.items():
        have = club_tokens(candidate_key)
        if not have:
            continue
        # Значимые слова запроса должны целиком входить в кандидата
        # ("barcelona" в "fc barcelona"), либо наоборот.
        if wanted <= have or have <= wanted:
            extra = len(have ^ wanted)
            matches.append((extra, candidate_key, club_id))

    if not matches:
        return None
    matches.sort()
    best_extra = matches[0][0]
    best = [m for m in matches if m[0] == best_extra]
    if len(best) > 1:
        return None  # неоднозначно - не угадываем
    return best[0][2]


# ---------------------------------------------------------------------------
# Поиск игрока в составе клуба назначения
# ---------------------------------------------------------------------------

_squad_cache: dict[str, list[dict]] = {}


def squad_players(club_id: str) -> list[dict]:
    if club_id in _squad_cache:
        return _squad_cache[club_id]
    squad = api("/club/%s/squad" % club_id)["data"]["squad"]
    ids = [row["playerId"] for row in squad]

    def one(player_id: str) -> dict | None:
        try:
            return api("/player/%s" % player_id)["data"]
        except Exception:
            return None

    with ThreadPoolExecutor(max_workers=6) as pool:
        players = [p for p in pool.map(one, ids) if p]
    _squad_cache[club_id] = players
    return players


_local_index: list[dict] | None = None

_LOCAL_BLOCK = re.compile(
    r'- name: "([^"]+)"\s*\n\s+position: "[^"]*"\s*\n\s+position_short: "[^"]*"'
    r'\s*\n\s+age: \d+\s*\n\s+value: "[^"]*"\s*\n\s+tm_id: "(\d+)"')


def local_player_index() -> list[dict]:
    """Игроки из наших же клубных страниц: имя, TM ID, текущий клуб.

    Для слуха клуб назначения — гипотеза, игрока там нет по определению,
    а прежний клуб в заголовке чаще всего не назван вовсе ("Liverpool target
    Minteh"). Искать его в API бесполезно: поиск по имени там не работает,
    возвращает ноль на любой запрос.

    Зато составы мы и так храним у себя — 4179 игроков из 148 клубов.
    Поиск по ним не стоит ни одного запроса в сеть и заодно даёт прежний клуб.
    """
    global _local_index
    if _local_index is not None:
        return _local_index
    rows: list[dict] = []
    clubs_dir = ACTIVE_PROJECT / "content" / "clubs"
    if clubs_dir.exists():
        for directory in sorted(clubs_dir.iterdir()):
            page = directory / "index.md"
            if not page.is_file():
                continue
            text = page.read_text(encoding="utf-8", errors="replace")
            club = re.search(r'(?m)^club_name:\s*"([^"]*)"', text)
            tm_club = re.search(r'(?m)^transfermarkt_club_id:\s*"(\d+)"', text)
            for match in _LOCAL_BLOCK.finditer(text):
                rows.append({
                    "name": match.group(1),
                    "tm_id": match.group(2),
                    "club": club.group(1) if club else directory.name,
                    "tm_club_id": tm_club.group(1) if tm_club else "",
                })
    _local_index = rows
    return rows


def resolve_local_player(candidate_name: str) -> dict | None:
    """Тот же порядок сопоставления, что и в составе: полное имя, потом фамилия."""
    rows = local_player_index()
    wanted_full = normalize(candidate_name)
    wanted_surname = surname(candidate_name)
    if not wanted_surname:
        return None
    exact = [r for r in rows if normalize(r["name"]) == wanted_full]
    if len(exact) == 1:
        return exact[0]
    by_surname = [r for r in rows if surname(r["name"]) == wanted_surname]
    if len(by_surname) == 1:
        return by_surname[0]
    if len(by_surname) > 1:
        return {"__ambiguous__": [r["name"] for r in by_surname]}
    return None


def match_player(players: list[dict], candidate_name: str) -> dict | None:
    """Сопоставление по фамилии, затем по полному имени."""
    wanted_surname = surname(candidate_name)
    wanted_full = normalize(candidate_name)
    if not wanted_surname:
        return None

    exact = [p for p in players if normalize(p.get("name", "")) == wanted_full]
    if len(exact) == 1:
        return exact[0]

    by_surname = [p for p in players if surname(p.get("name", "")) == wanted_surname]
    if len(by_surname) == 1:
        return by_surname[0]
    if len(by_surname) > 1:
        # Несколько однофамильцев в одном составе - однозначно не выбрать.
        return {"__ambiguous__": [p["name"] for p in by_surname]}

    # Фамилия из заголовка может быть частью составного имени игрока.
    partial = [p for p in players if wanted_surname in normalize(p.get("name", "")).split()]
    if len(partial) == 1:
        return partial[0]
    return None


# ---------------------------------------------------------------------------
# Дедупликация по Transfermarkt ID
# ---------------------------------------------------------------------------

def site_tm_ids() -> dict[str, str]:
    """transfermarkt_player_id -> slug на сайте."""
    data = json.loads(
        (ACTIVE_PROJECT / "data" / "transfers.json").read_text(encoding="utf-8"))
    result: dict[str, str] = {}
    for row in data:
        if not isinstance(row, dict):
            continue
        tm_id = row.get("transfermarkt_player_id") or row.get("player_id")
        if tm_id:
            result[str(tm_id)] = row.get("slug") or row.get("player") or "?"
    return result


def market_points(details: dict) -> list[dict]:
    """Реальные чекпоинты Transfermarkt. Ничего не интерполируем."""
    seen: dict[tuple[str, float], dict] = {}
    for key in ("highest", "previous", "current"):
        value = (details or {}).get(key) or {}
        if value.get("value") and value.get("determined"):
            millions = round(value["value"] / 1_000_000, 2)
            seen[(value["determined"], millions)] = {
                "date": value["determined"],
                "value_eur_m": millions,
            }
    return sorted(seen.values(), key=lambda p: p["date"])


# ---------------------------------------------------------------------------

def enrich_record(record: dict, tm_clubs: dict[str, str],
                  known_ids: dict[str, str]) -> dict:
    previous_state = record.get("pipeline_state") or ""
    record = dict(record)
    record["enriched_at"] = now_iso()
    # found_in описывает результат ЭТОГО прогона, а не хранимое состояние.
    # Оставшись с прошлого раза ("from_club", когда игрок ещё числился в
    # прежнем клубе), значение навсегда блокировало условие повышения ниже —
    # и слух не мог стать трансфером, даже когда переход состоялся.
    record.pop("found_in", None)

    club_id = resolve_tm_club(record["to_club"], tm_clubs)
    if not club_id:
        record["pipeline_state"] = "NEEDS_REVIEW"
        record["block_reason"] = "TM_CLUB_UNRESOLVED"
        record["block_detail"] = "клуб назначения %r не найден в справочнике TM" % record["to_club"]
        return record
    record["tm_to_club_id"] = club_id

    try:
        players = squad_players(club_id)
    except Exception as error:
        record["pipeline_state"] = "RETRY"
        record["block_reason"] = "TM_SQUAD_UNAVAILABLE"
        record["block_detail"] = str(error)[:120]
        return record

    matched = match_player(players, record["player"])

    if matched and "__ambiguous__" in matched:
        record["pipeline_state"] = "NEEDS_REVIEW"
        record["block_reason"] = "AMBIGUOUS_PLAYER"
        record["block_detail"] = "однофамильцы в составе: %s" % ", ".join(
            matched["__ambiguous__"])
        return record

    if not matched and record.get("kind") == "agreement":
        # Договорённости в составе нового клуба и не должно быть.
        # Ищем игрока в ПРЕЖНЕМ клубе: он там ещё числится, и это даёт
        # полноценную идентичность для страницы слуха.
        from_club_id = resolve_tm_club(record.get("from_club") or "", tm_clubs)
        if from_club_id:
            try:
                matched = match_player(squad_players(from_club_id), record["player"])
            except Exception:
                matched = None
            if matched and "__ambiguous__" in matched:
                matched = None
            if matched:
                record["tm_from_club_id"] = from_club_id
                record["found_in"] = "from_club"

    if not matched and record.get("kind") in ("rumour", "negotiations"):
        # Слух: игрока в составе клуба назначения быть и не должно.
        # Личность берём из локального индекса составов, оттуда же —
        # прежний клуб, если в заголовке его не назвали.
        local = resolve_local_player(record["player"])
        if local and "__ambiguous__" in local:
            record["pipeline_state"] = "NEEDS_REVIEW"
            record["block_reason"] = "AMBIGUOUS_PLAYER"
            record["block_detail"] = "однофамильцы в наших составах: %s" % ", ".join(
                local["__ambiguous__"])
            return record
        if local:
            try:
                matched = api("/player/%s" % local["tm_id"])["data"]
            except Exception as error:
                record["pipeline_state"] = "RETRY"
                record["block_reason"] = "TM_PLAYER_UNAVAILABLE"
                record["block_detail"] = str(error)[:120]
                return record
            record["found_in"] = "local_index"
            record["tm_from_club_id"] = local["tm_club_id"]
            if not record.get("from_club"):
                record["from_club"] = local["club"]

    if not matched:
        if record.get("kind") in ("rumour", "negotiations"):
            record["pipeline_state"] = "NEEDS_REVIEW"
            record["block_reason"] = "RUMOUR_PLAYER_UNKNOWN"
            record["block_detail"] = (
                "%s не найден ни в составе %s, ни в наших 148 составах — "
                "личность не подтверждена" % (record["player"], record["to_club"]))
            return record
        if record.get("kind") == "agreement":
            record["pipeline_state"] = (
                previous_state if previous_state == "PUBLISHED_AS_RUMOR"
                else "AWAITING_CONFIRMATION")
            record["block_reason"] = "AGREEMENT_NOT_YET_COMPLETED"
            record["block_detail"] = (
                "%s пока не числится в составе %s. Это договорённость, "
                "а не состоявшийся переход." % (record["player"], record["to_club"]))
            return record
        record["pipeline_state"] = "NEEDS_REVIEW"
        record["block_reason"] = "PLAYER_NOT_IN_DESTINATION_SQUAD"
        record["block_detail"] = (
            "%s не числится в составе %s на Transfermarkt - "
            "переход не подтверждён" % (record["player"], record["to_club"]))
        return record

    if record.get("kind") == "agreement" and record.get("found_in") != "from_club":
        # Игрок найден в составе клуба НАЗНАЧЕНИЯ - значит договорённость
        # превратилась в состоявшийся переход. Повышаем статус.
        record["kind"] = "official"
        record["promoted_from_agreement_at"] = now_iso()
        record["promotion_evidence"] = (
            "числится в составе %s на Transfermarkt" % record["to_club"])

    attributes = matched.get("attributes") or {}
    life = matched.get("lifeDates") or {}
    position = attributes.get("position") or {}

    record["tm_player_id"] = str(matched["id"])
    record["player_full_name"] = matched.get("name") or record["player"]
    record["birth_date"] = life.get("dateOfBirth") or ""
    record["age"] = life.get("age")
    record["position"] = position.get("name") or attributes.get("positionGroupName") or ""
    record["position_short"] = position.get("shortName") or ""
    record["preferred_foot"] = (attributes.get("preferredFoot") or {}).get("name") or ""
    record["height"] = attributes.get("height")
    record["contract_until"] = attributes.get("contractUntil") or ""
    record["portrait_url"] = matched.get("portraitUrl") or ""
    record["market_value_points"] = market_points(matched.get("marketValueDetails") or {})
    record["nationality_ids"] = (matched.get("nationalityDetails") or {}).get(
        "nationalities") or {}

    # Дополнительный фактический материал для статьи.
    birth = matched.get("birthPlaceDetails") or {}
    record["birth_place"] = birth.get("placeOfBirth") or ""
    record["former_clubs_note"] = attributes.get("formerClubsNote") or ""

    assignments = matched.get("clubAssignments") or []
    current = next((a for a in assignments if a.get("type") == "current"), {})
    national = next((a for a in assignments if a.get("type") == "nationalTeam"), {})
    record["shirt_number"] = current.get("shirtNumber")
    record["is_captain"] = bool(current.get("isCaptain"))
    record["transfer_date"] = current.get("start") or ""
    record["national_team_debut"] = national.get("debut") or ""

    # Аналитика по составу. Данные уже загружены выше, доп. запросов нет.
    def value_of(person: dict) -> float:
        current = ((person.get("marketValueDetails") or {}).get("current") or {})
        return float(current.get("value") or 0)

    same_position = [
        p for p in players
        if ((p.get("attributes") or {}).get("position") or {}).get("name")
        == (matched.get("attributes") or {}).get("position", {}).get("name")
        and str(p.get("id")) != str(matched["id"])
    ]
    ranked = sorted(players, key=value_of, reverse=True)
    ages = [((p.get("lifeDates") or {}).get("age") or 0) for p in players]
    ages = [a for a in ages if a]
    own_age = (matched.get("lifeDates") or {}).get("age") or 0
    record["squad_analysis"] = {
        "same_position_count": len(same_position),
        "same_position_names": [p.get("name") for p in same_position][:4],
        "value_rank": next((i + 1 for i, p in enumerate(ranked)
                            if str(p.get("id")) == str(matched["id"])), None),
        "squad_total": len(players),
        "younger_than": sum(1 for a in ages if a > own_age) if own_age else 0,
    }

    try:
        club = api("/club/%s" % club_id)["data"]
        squad_details = club.get("squadDetails") or {}
        superior = (club.get("baseDetails") or {}).get("superiorClub") or {}
        record["to_club_official_name"] = club.get("name") or record["to_club"]
        record["to_club_context"] = {
            "squad_size": squad_details.get("squadSize"),
            "average_age": squad_details.get("averageAgeDisplay"),
            "squad_value": ((squad_details.get("currentMarketValue") or {})
                            .get("compact") or {}),
            "average_player_value": ((squad_details.get("averageMarketValue") or {})
                                     .get("compact") or {}),
            "stadium": (superior.get("location") or {}).get("street") or "",
            "city": (superior.get("location") or {}).get("city") or "",
        }
    except Exception:
        record["to_club_context"] = {}

    if not record["portrait_url"]:
        record["pipeline_state"] = "RETRY"
        record["block_reason"] = "BLOCKED_NO_PLAYER_PHOTO"
        record["block_detail"] = "портрет на Transfermarkt ещё не опубликован"
        return record

    # Настоящая дедупликация: по Transfermarkt ID, а не по имени.
    existing = known_ids.get(record["tm_player_id"])
    if existing:
        record["verdict"] = "DUPLICATE_EXISTING"
        record["verdict_reason"] = "TM ID %s уже на сайте: %s" % (
            record["tm_player_id"], existing)
        record["pipeline_state"] = "SKIPPED_DUPLICATE"
        return record

    record["verdict"] = "NEW_CANDIDATE"
    record["verdict_reason"] = ""
    record["block_reason"] = ""
    record["block_detail"] = ""
    if record.get("kind") in ("agreement", "negotiations", "rumour"):
        # Данные собраны, но переход не состоялся: материал для раздела Слухи.
        # Уже опубликованный слух повторно не публикуем: состояние сохраняем,
        # иначе каждый прогон переписывал бы страницу заново.
        if previous_state != "PUBLISHED_AS_RUMOR":
            record["pipeline_state"] = "RUMOR_READY"
    else:
        record["pipeline_state"] = "ENRICHED"
    return record


def run(save: bool, only_official: bool = True, refresh_clubs: bool = False) -> dict:
    tm_clubs = build_tm_club_index(refresh=refresh_clubs)
    known_ids = site_tm_ids()
    print("  TM ID уже на сайте: %d" % len(known_ids))

    records = []
    for path in sorted(RECORDS_DIR.glob("*.json")):
        try:
            record = json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            continue
        if record.get("schema_version") != 2:
            continue
        # Договорённости проверяем тоже: именно так ловится момент,
        # когда сделка закрылась и её уже можно публиковать.
        if only_official and record.get("kind") not in ("official", "agreement"):
            continue
        records.append((path, record))

    print("  кандидатов к обогащению: %d\n" % len(records))
    results = []
    for path, record in records:
        enriched = enrich_record(record, tm_clubs, known_ids)
        results.append(enriched)
        if save:
            path.write_text(json.dumps(enriched, ensure_ascii=False, indent=2) + "\n",
                            encoding="utf-8")
    return {"results": results}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Promyachik transfer enrichment (read-only)")
    parser.add_argument("--save", action="store_true",
                        help="записать обогащённые записи обратно")
    parser.add_argument("--all-kinds", action="store_true",
                        help="обогащать не только состоявшиеся переходы")
    parser.add_argument("--refresh-clubs", action="store_true",
                        help="перестроить справочник клубов TM")
    args = parser.parse_args(argv)

    print("\n=== ОБОГАЩЕНИЕ (сайт не изменялся) ===")
    result = run(save=args.save, only_official=not args.all_kinds,
                 refresh_clubs=args.refresh_clubs)

    ready, blocked = [], []
    for record in result["results"]:
        (ready if record["pipeline_state"] == "ENRICHED" else blocked).append(record)

    if ready:
        print("--- ГОТОВЫ К ПУБЛИКАЦИИ: %d ---" % len(ready))
        for record in ready:
            points = record.get("market_value_points") or []
            print("  %s (TM %s)" % (record["player_full_name"], record["tm_player_id"]))
            print("     %s -> %s | %s | %s | точек графика: %d" % (
                record["from_club"] or "?", record["to_club"],
                record.get("position") or "?",
                record.get("birth_date") or "?", len(points)))

    if blocked:
        print("\n--- НЕ ПРОШЛИ: %d ---" % len(blocked))
        for record in blocked:
            print("  [%s] %s : %s" % (
                record.get("block_reason") or record["pipeline_state"],
                record["player"],
                record.get("block_detail") or record.get("verdict_reason") or ""))
    print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
