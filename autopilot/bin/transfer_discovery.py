"""
PROMYACHIK TRANSFER AUTOPILOT - DISCOVERY (read-only)

Читает RSS официальных СМИ, выделяет события трансферного характера,
нормализует их и сверяет с живым сайтом.

Ключевой принцип фильтрации: извлечённый клуб обязан резолвиться по
справочнику реальных клубов. Заголовок, в котором ни один клуб не опознан,
кандидатом не считается. Это отсекает "elite 250 club", крикет и хвосты
вроде "PSG in 123m move" надёжнее любых регулярных выражений.

Ничего не публикует и не изменяет Promyachik_CLEAN.
"""
from __future__ import annotations

import argparse
import json
import re
import ssl
import unicodedata
import urllib.request
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from html import unescape
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from paths import SITE as ACTIVE_PROJECT, WORK as PROFUTBIK  # noqa: E402
PARSER_ROOT = PROFUTBIK / "parser"
RECORDS_DIR = PARSER_ROOT / "state" / "records"
HISTORY_DIR = PARSER_ROOT / "state" / "history"

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36"
)

FEEDS = [
    {"id": "bbc-sport-football", "publisher": "BBC Sport", "lang": "en",
     "url": "https://feeds.bbci.co.uk/sport/football/rss.xml", "tier": "major_media"},
    {"id": "guardian-football", "publisher": "The Guardian", "lang": "en",
     "url": "https://www.theguardian.com/football/rss", "tier": "major_media"},
    {"id": "sky-sports", "publisher": "Sky Sports", "lang": "en",
     "url": "https://feeds.skynews.com/feeds/rss/sports.xml", "tier": "major_media"},
    {"id": "championat-football", "publisher": "Championat", "lang": "ru",
     "url": "https://www.championat.com/rss/news/football/", "tier": "major_media"},
]

# Разговорные формы, которых нет в каталоге логотипов.
CLUB_ALIASES = {
    "psg": "Paris Saint Germain",
    "paris st germain": "Paris Saint Germain",
    "man city": "Manchester City",
    "man utd": "Manchester United",
    "man united": "Manchester United",
    "spurs": "Tottenham",
    "barca": "Barcelona",
    "juve": "Juventus",
    "atleti": "Atletico Madrid",
    "atletico": "Atletico Madrid",
    "real": "Real Madrid",
    "inter milan": "Inter",
    "bayern": "Bayern Munich",
    "dortmund": "Borussia Dortmund",
    "leverkusen": "Bayer Leverkusen",
    "wolves": "Wolves",
    "leeds": "Leeds",
    "forest": "Nottingham Forest",
    "brighton": "Brighton",
    "newcastle": "Newcastle",
    "villa": "Aston Villa",
}

# Глаголы завершённого перехода.
COMPLETED_RE = re.compile(
    r"\b(signs?|signed|joins?|joined|completes?\s+(?:a\s+)?move|"
    r"completes?\s+(?:the\s+)?signing|seals?\s+(?:a\s+)?move|unveiled)\b", re.I)

# Договорённость / переговоры - это ещё не переход.
AGREEMENT_RE = re.compile(
    r"\b(agree[sd]?\s+(?:terms|deal|to\s+sign|personal\s+terms)|"
    r"agreement|set\s+to\s+(?:sign|join)|expected\s+to\s+(?:sign|join)|"
    r"close\s+to|nearing|on\s+the\s+verge|medical)\b", re.I)

INTEREST_RE = re.compile(
    r"\b(eye|eyeing|eyes|target|targeting|targets|want|wants|interest|interested|"
    r"talks|bid|bids|approach|linked|considering|monitor|monitoring|pursue|"
    r"chase|chasing|rumours?|gossip)\b", re.I)

INTEREST_RE_RU = re.compile(
    "намерен|хочет|интересуется|переговор|предлож|слух|может перейти|"
    "нацелен|рассматривает", re.I)

# Заведомо не трансферные материалы.
NOISE = re.compile(
    r"\b(preview|report\s*card|match\s+report|highlights|quiz|podcast|"
    r"predictions?|ratings?|opinion|column|analysis|women'?s|under-?\d+|"
    r"injury|injured|banned|charged|sacked|appointed|head\s+coach|manager|"
    r"table|fixtures?|results?|kick-?off|watch|video|what\s+happened)\b", re.I)

NOISE_RU = re.compile("обзор|прогноз|интервью|трансляц|результат|расписан", re.I)

# Виды спорта, которые нам не нужны.
OTHER_SPORTS = re.compile(
    r"\b(cricket|big\s+bash|rugby|nfl|nba|tennis|golf|f1|formula\s*1|"
    r"boxing|ufc|darts|snooker|cycling|athletics|baseball|hockey)\b", re.I)

# Приставки-описания перед именем игрока.
PLAYER_PREFIX = re.compile(
    r"^(?:[A-Z][a-z]+(?:'s|s')\s+)+", re.U)

PLAYER_SUFFIX = re.compile(
    r"\s+(?:on\s+loan|on\s+a\s+free|on\s+deadline\s+day|in\s+.*|for\s+.*)$", re.I)

FEE_RE = re.compile(r"[\u00a3\u20ac$]\s?\d[\d.,]*\s?(?:m|bn)?", re.I)


def to_iso(value: str) -> str:
    """RFC822 из RSS -> ISO. Пустая строка, если дата не разбирается."""
    if not value:
        return ""
    try:
        return parsedate_to_datetime(value).astimezone(timezone.utc).isoformat()
    except Exception:
        pass
    match = re.search(r"\d{4}-\d{2}-\d{2}", value)
    return match.group(0) if match else ""


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def fetch(url: str) -> bytes:
    request = urllib.request.Request(url, headers={
        "User-Agent": USER_AGENT,
        "Accept": "application/rss+xml,application/xml,text/xml,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9,ru;q=0.8",
    })
    with urllib.request.urlopen(
            request, timeout=30, context=ssl.create_default_context()) as response:
        return response.read()


def strip_tags(value: str) -> str:
    return re.sub(r"<[^>]+>", "", value or "").strip()


def parse_feed(xml: str) -> list[dict]:
    """Минимальный разбор RSS/Atom без внешних зависимостей."""
    items: list[dict] = []
    blocks = (re.findall(r"<item[ >].*?</item>", xml, re.S)
              or re.findall(r"<entry[ >].*?</entry>", xml, re.S))
    for block in blocks:
        def field(name: str) -> str:
            match = re.search(
                r"<%s[^>]*>(?:<!\[CDATA\[)?(.*?)(?:\]\]>)?</%s>" % (name, name),
                block, re.S)
            return unescape(strip_tags(match.group(1))) if match else ""

        link = field("link")
        if not link:
            match = re.search(r'<link[^>]*href="([^"]+)"', block)
            link = match.group(1) if match else ""
        title = field("title")
        if title:
            items.append({
                "title": title,
                "link": link,
                "published": field("pubDate") or field("updated") or field("published"),
                "summary": field("description") or field("summary"),
            })
    return items


def normalize(value: str) -> str:
    value = unicodedata.normalize("NFD", str(value or ""))
    value = value.encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", " ", value.lower()).strip()


def slugify(value: str) -> str:
    return re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", normalize(value))).strip("-")


# ---------------------------------------------------------------------------
# Справочник клубов
# ---------------------------------------------------------------------------

def build_club_index() -> dict[str, str]:
    """normalized alias -> каноническое имя клуба."""
    data = json.loads(
        (ACTIVE_PROJECT / "data" / "club-logos.json").read_text(encoding="utf-8"))
    clubs = data.get("clubs", data)
    index: dict[str, str] = {}
    if isinstance(clubs, dict):
        for entry in clubs.values():
            name = str((entry or {}).get("name") or "").strip()
            if name:
                index[normalize(name)] = name
    for alias, canonical in CLUB_ALIASES.items():
        index.setdefault(normalize(alias), canonical)
    return index


def resolve_club(text: str, index: dict[str, str]) -> str | None:
    """Ищет в тексте самое длинное known-club совпадение по границам слов."""
    haystack = normalize(text)
    if not haystack:
        return None
    best_alias = ""
    best_name = None
    for alias, canonical in index.items():
        if len(alias) < 3 or len(alias) <= len(best_alias):
            continue
        if re.search(r"(?:^| )%s(?:$| )" % re.escape(alias), haystack):
            best_alias, best_name = alias, canonical
    return best_name


def clean_player(value: str) -> str:
    value = (value or "").strip()
    # Отрезаем только отбивку " - ", не дефис внутри фамилии.
    value = re.split(r"\s+[-\u2013\u2014]\s+", value)[0]
    value = re.split(r"\s*[:|]\s*", value)[0]
    value = PLAYER_PREFIX.sub("", value)
    value = PLAYER_SUFFIX.sub("", value)
    return value.strip(" .,\"'\u00ab\u00bb")


def looks_like_person(name: str, index: dict[str, str]) -> bool:
    if not name or len(name) < 3:
        return False
    words = name.split()
    if not (1 <= len(words) <= 4):
        return False
    if re.search(r"\d", name):
        return False
    if normalize(name) in index:          # это клуб, а не человек
        return False
    if not name[0].isupper():
        return False
    return True


# ---------------------------------------------------------------------------
# Классификация
# ---------------------------------------------------------------------------

EXTRACT_PATTERNS = [
    # "Newcastle sign Fernandez-Pardo from Lille for £51m"
    (re.compile(r"^(?P<to>.+?)\s+(?:sign|signs|land)\s+(?P<player>.+?)"
                r"\s+from\s+(?P<from>.+?)$", re.I), "club_first"),
    # "Juventus agree to sign Woltemade on loan from Newcastle"
    (re.compile(r"^(?P<to>.+?)\s+agree.{0,20}?\s+sign\s+(?P<player>.+?)"
                r"\s+from\s+(?P<from>.+?)$", re.I), "club_first"),
    # "Barcola joins Liverpool from PSG in £123m move"
    (re.compile(r"^(?P<player>.+?)\s+(?:joins|signs\s+for|completes\s+move\s+to|"
                r"seals\s+move\s+to)\s+(?P<to>.+?)\s+from\s+(?P<from>.+?)$", re.I),
     "player_first"),
    # "Germany's Wamser completes move to Man City"
    (re.compile(r"^(?P<player>.+?)\s+(?:joins|signs\s+for|completes\s+move\s+to|"
                r"seals\s+move\s+to)\s+(?P<to>.+?)$", re.I), "player_first"),
    # "Barcola leaves PSG for Liverpool"
    (re.compile(r"^(?P<player>.+?)\s+leaves\s+(?P<from>.+?)\s+for\s+(?P<to>.+?)$", re.I),
     "player_first"),
]


# Грамматика слухов отличается от грамматики перехода. Про состоявшийся
# трансфер пишут "клуб подписал игрока из клуба", а про слух — "клуб положил
# глаз на игрока" или "игрока предложили клубу". Шаблоны выше на второй
# конструкции не срабатывали, и слухи уходили в отказ как "без структуры":
# сайт мог показывать только то, что уже случилось.
#
# Имя игрока ловим как одно-три слова с заглавной, а не как ".+?" — иначе в
# него утекает хвост заголовка ("Minteh can still get dream move").
_NAME = r"[A-Z][\w'’\-]+(?:\s+[A-Z][\w'’\-]+){0,2}"
_CLUB = r"[A-Z][\w'’&\.\-]*(?:\s+[A-Z][\w'’&\.\-]*){0,3}"

RUMOUR_PATTERNS = [
    # "Bissouma was offered to Chelsea"
    (re.compile(r"^(?P<player>%s)\s+(?:was\s+|has\s+been\s+|is\s+)?offered\s+to\s+"
                r"(?P<to>%s)\b" % (_NAME, _CLUB)), "negotiations"),
    # "Chelsea make bid for Osimhen" / "Chelsea in talks for ..."
    (re.compile(r"^(?P<to>%s)\s+(?:make|makes|made|in|open|hold|holds|held)\s+"
                r"(?:a\s+|the\s+)?(?:bid|talks|approach|move|offer)\s+"
                r"(?:for|over|with)\s+(?P<player>%s)\b" % (_CLUB, _NAME)), "negotiations"),
    # "Rashford linked with a move to Barcelona"
    (re.compile(r"^(?P<player>%s)\s+linked\s+with\s+(?:a\s+move\s+to\s+)?"
                r"(?P<to>%s)\b" % (_NAME, _CLUB)), "rumour"),
    # "Player wants move to Chelsea"
    (re.compile(r"^(?P<player>%s)\s+wants?\s+(?:a\s+)?move\s+to\s+"
                r"(?P<to>%s)\b" % (_NAME, _CLUB)), "rumour"),
    # "Liverpool target Minteh"
    (re.compile(r"^(?P<to>%s)\s+targets?\s+(?P<player>%s)\b" % (_CLUB, _NAME)), "rumour"),
    # "Arsenal eye Nico Williams"
    (re.compile(r"^(?P<to>%s)\s+(?:eye|eyes|eyeing|want|wants|chase|chasing|"
                r"pursue|pursuing|monitor|monitoring|track|tracking)\s+"
                r"(?P<player>%s)\b" % (_CLUB, _NAME)), "rumour"),
    # "Rangers failed to pursue Ferguson"
    (re.compile(r"^(?P<to>%s)\s+(?:failed\s+to\s+)?pursue\s+"
                r"(?P<player>%s)\b" % (_CLUB, _NAME)), "rumour"),
]


def classify_rumour(text: str, index: dict[str, str]) -> tuple[str, dict | None, str]:
    """Разбор слуха. Клуб прежний из заголовка обычно неизвестен — это нормально.

    Проверки те же, что для переходов: имя должно быть похоже на человека,
    клуб — резолвиться по справочнику. Именно они отсеивают Формулу-1,
    бокс и отчёты о матчах, где слова-маркеры есть, а сущностей нет.
    """
    for pattern, stage in RUMOUR_PATTERNS:
        match = pattern.match(text)
        if not match:
            continue
        groups = match.groupdict()
        player = clean_player(groups.get("player") or "")
        if not looks_like_person(player, index):
            continue
        to_club = resolve_club(groups.get("to") or "", index)
        if not to_club:
            continue
        fee_match = FEE_RE.search(text)
        return stage, {
            "player": player,
            "from_club": "",
            "to_club": to_club,
            "fee_raw": fee_match.group(0) if fee_match else "",
        }, ""
    return "rumour", None, "слух без разбираемой структуры"


def classify(title: str, index: dict[str, str]) -> tuple[str, dict | None, str]:
    """Возвращает (kind, extracted, reject_reason).

    kind: official | agreement | rumour | ignore
    """
    text = title.strip()

    if OTHER_SPORTS.search(text):
        return "ignore", None, "другой вид спорта"
    if NOISE.search(text) or NOISE_RU.search(text):
        return "ignore", None, "нетрансферный материал"

    for pattern, order in EXTRACT_PATTERNS:
        match = pattern.match(text)
        if not match:
            continue
        groups = match.groupdict()
        player = clean_player(groups.get("player") or "")
        if not looks_like_person(player, index):
            continue

        to_club = resolve_club(groups.get("to") or "", index)
        from_club = resolve_club(groups.get("from") or "", index)
        if not to_club:
            return "ignore", None, "клуб назначения не опознан: %r" % (
                (groups.get("to") or "")[:40])

        # Договорённость - ещё не переход.
        if AGREEMENT_RE.search(text) and not COMPLETED_RE.search(
                text[:text.lower().find("agree")] if "agree" in text.lower() else ""):
            kind = "agreement"
        elif COMPLETED_RE.search(text):
            kind = "official"
        else:
            kind = "agreement"

        fee_match = FEE_RE.search(text)
        return kind, {
            "player": player,
            "from_club": from_club or "",
            "to_club": to_club,
            "fee_raw": fee_match.group(0) if fee_match else "",
        }, ""

    if INTEREST_RE.search(text) or INTEREST_RE_RU.search(text):
        return classify_rumour(text, index)

    return "ignore", None, "структура не распознана"


def entity_id(player: str, from_club: str, to_club: str) -> str:
    parts = [slugify(player), slugify(from_club) or "unknown", slugify(to_club)]
    return "__".join(part for part in parts if part)


# ---------------------------------------------------------------------------
# Дедупликация против живого сайта - только структурная идентичность
# ---------------------------------------------------------------------------

def surname(value: str) -> str:
    """Последнее слово имени. СМИ часто дают только фамилию."""
    parts = normalize(value).split()
    return parts[-1] if parts else ""


def load_site_index() -> dict:
    data = json.loads(
        (ACTIVE_PROJECT / "data" / "transfers.json").read_text(encoding="utf-8"))
    players: set[str] = set()
    slugs: set[str] = set()
    # фамилия -> список "полное имя -> клуб назначения" для внятного сообщения
    surnames: dict[str, list[str]] = {}
    for row in data:
        if not isinstance(row, dict):
            continue
        name = row.get("player") or row.get("player_name") or ""
        if name:
            players.add(normalize(name))
            surnames.setdefault(surname(name), []).append(
                "%s -> %s" % (name, row.get("to_club_name") or row.get("to_name") or "?"))
        if row.get("slug"):
            slugs.add(row["slug"])
    pages = {p.name for p in (ACTIVE_PROJECT / "content" / "transfers").iterdir()
             if p.is_dir()}
    return {"players": players, "slugs": slugs, "pages": pages,
            "surnames": surnames}


def dedup_verdict(site: dict, player: str, to_club: str) -> tuple[str, str]:
    slug = "%s-%s" % (slugify(player), slugify(to_club))
    if slug in site["slugs"] or slug in site["pages"]:
        return "DUPLICATE_EXISTING", "slug %s уже есть на сайте" % slug
    if normalize(player) in site["players"]:
        return "POSSIBLE_DUPLICATE", "игрок %s уже фигурирует в transfers.json" % player

    # СМИ часто дают только фамилию: "Barcola" против "Bradley Barcola" на сайте.
    # Фамилии не уникальны, поэтому это подозрение, а не жёсткий дубль.
    matches = site["surnames"].get(surname(player)) or []
    if matches:
        same_club = [m for m in matches
                     if normalize(to_club) and normalize(to_club) in normalize(m)]
        if same_club:
            return "DUPLICATE_EXISTING", (
                "фамилия и клуб совпали с существующим: %s" % "; ".join(same_club))
        return "POSSIBLE_DUPLICATE", (
            "совпала фамилия с: %s" % "; ".join(matches))

    return "NEW_CANDIDATE", ""


# ---------------------------------------------------------------------------

def discover(save: bool, verbose: bool = False) -> dict:
    site = load_site_index()
    clubs = build_club_index()
    RECORDS_DIR.mkdir(parents=True, exist_ok=True)
    HISTORY_DIR.mkdir(parents=True, exist_ok=True)

    stats = {"feeds_ok": 0, "feeds_failed": 0, "items": 0,
             "official": 0, "agreement": 0, "negotiations": 0,
             "rumour": 0, "ignore": 0}
    found: list[dict] = []
    rejected: list[tuple[str, str]] = []
    seen: set[str] = set()

    for feed in FEEDS:
        try:
            raw = fetch(feed["url"])
            stats["feeds_ok"] += 1
        except Exception as error:
            stats["feeds_failed"] += 1
            print("  FEED FAIL %s: %s" % (feed["id"], str(error)[:70]))
            continue

        items = parse_feed(raw.decode("utf-8", "replace"))
        stats["items"] += len(items)

        for item in items:
            kind, extracted, reason = classify(item["title"], clubs)
            stats[kind] += 1
            if not extracted:
                if verbose and kind != "ignore":
                    rejected.append((item["title"], reason))
                continue

            eid = entity_id(extracted["player"], extracted["from_club"],
                            extracted["to_club"])
            if eid in seen:
                continue
            seen.add(eid)

            verdict, verdict_reason = dedup_verdict(
                site, extracted["player"], extracted["to_club"])

            record = {
                "schema_version": 2,
                "kind": kind,
                "entity_id": eid,
                "player": extracted["player"],
                "from_club": extracted["from_club"],
                "to_club": extracted["to_club"],
                "fee_raw": extracted["fee_raw"],
                "verdict": verdict,
                "verdict_reason": verdict_reason,
                "pipeline_state": "DISCOVERED",
                "source": {
                    "publisher": feed["publisher"],
                    "tier": feed["tier"],
                    "url": item["link"],
                    "title": item["title"],
                    "published": item["published"],
                    "published_iso": to_iso(item["published"]),
                },
                "discovered_at": now_iso(),
            }
            found.append(record)

            if save:
                path = RECORDS_DIR / ("%s.json" % eid)
                path.write_text(
                    json.dumps(record, ensure_ascii=False, indent=2) + "\n",
                    encoding="utf-8")

    return {"stats": stats, "found": found, "rejected": rejected}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Promyachik transfer discovery (read-only)")
    parser.add_argument("--save", action="store_true",
                        help="сохранить найденное в parser/state/records")
    parser.add_argument("--json", action="store_true", help="машиночитаемый вывод")
    parser.add_argument("--verbose", action="store_true",
                        help="показать отклонённые заголовки и причины")
    args = parser.parse_args(argv)

    result = discover(save=args.save, verbose=args.verbose)

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0

    stats = result["stats"]
    print("\n=== РАЗВЕДКА (сайт не изменялся) ===")
    print("  фидов ok/fail   : %s/%s" % (stats["feeds_ok"], stats["feeds_failed"]))
    print("  заголовков      : %s" % stats["items"])
    print("  переходы        : %s" % stats["official"])
    print("  договорённости  : %s" % stats["agreement"])
    print("  переговоры      : %s" % stats["negotiations"])
    print("  слухи           : %s" % stats["rumour"])
    print("  отсеяно         : %s" % stats["ignore"])

    labels = {"NEW_CANDIDATE": "НОВЫЙ",
              "DUPLICATE_EXISTING": "есть на сайте",
              "POSSIBLE_DUPLICATE": "возможно дубль"}
    headings = {"official": "СОСТОЯВШИЕСЯ ПЕРЕХОДЫ",
                "agreement": "ДОГОВОРЁННОСТИ (не переход)",
                "negotiations": "ПЕРЕГОВОРЫ",
                "rumour": "СЛУХИ"}

    for kind in ("official", "agreement", "negotiations", "rumour"):
        rows = [row for row in result["found"] if row["kind"] == kind]
        if not rows:
            continue
        print("\n--- %s: %d ---" % (headings[kind], len(rows)))
        for row in rows:
            fee = " | %s" % row["fee_raw"] if row["fee_raw"] else ""
            print("  [%14s] %s : %s -> %s%s" % (
                labels[row["verdict"]], row["player"],
                row["from_club"] or "?", row["to_club"], fee))
            print("                   %s: %s" % (
                row["source"]["publisher"], row["source"]["title"][:78]))

    if args.verbose and result["rejected"]:
        print("\n--- ОТКЛОНЕНО (%d) ---" % len(result["rejected"]))
        for title, reason in result["rejected"][:25]:
            print("  %s\n      причина: %s" % (title[:76], reason))
    print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
