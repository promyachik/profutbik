"""
PF517C — СОСТАВЫ ВОСЬМИ ЛИГ НА ТЕКУЩИЙ СЕЗОН

Зачем. `data/club-logos.json` собран под сезон 2024 и с тех пор пополнялся
поштучно: когда трансфер приводил незнакомый клуб, движок дописывал его ради
эмблемы, а `league_id` заполнить было неоткуда — запрос шёл по названию, не по
лиге. Накопилось 37 клубов без лиги, и не только «Аль-Хиляль», которому там и
место, но и те, кто играет у нас прямо сейчас. Обратная беда тоже есть: у
вылетевших с 2024 года лига осталась прежней. Пока лига нигде не
использовалась, это было незаметно; как только выпадающий список на
`/transfers/` стал по ней фильтровать, дыра вылезла наружу.

Почему не API-Football. Бесплатный план отдаёт составы лиг только за сезоны
2022–2024: «Free plans do not have access to this season». Из-за этого
справочник и застрял. Берём открытый API Transfermarkt, которым уже
пользуется движок: `/competition/<code>/table` отдаёт состав текущего сезона,
`/club/<id>` — название, короткое название и аббревиатуру.

Почему отдельный файл, а не правка club-logos.json. Клубы двух справочников
сводятся по названию, а названия у провайдеров разные: «Stade Rennais FC» и
«Rennes», «Kasimpasa» и «Kasımpaşa». Часть пар не сходится, и если бы скрипт
писал прямо в общий справочник, несошедшийся клуб терял бы лигу — то есть
ошибка сопоставления выглядела бы как вылет из лиги. Здесь результат ложится
рядом, в `data/club_leagues.json`; шаблон сначала смотрит туда, а для клубов,
которых там нет, берёт прежнее значение. Худшее, что даёт промах, — клуб
остаётся с прошлогодней лигой, а не исчезает из всех.

Запуск:
    python refresh_club_leagues.py            показать, что получится
    python refresh_club_leagues.py --save     записать
"""
from __future__ import annotations

import argparse
import json
import re
import ssl
import sys
import time
import unicodedata
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from paths import SITE, CACHE_DIR  # noqa: E402

# Консоль на машине Дмитрия работает в cp1251 и падает на «Süper Lig».
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

CLUB_DIRECTORY = SITE / "data" / "club-logos.json"
OUTPUT = SITE / "data" / "club_leagues.json"
ROSTER_CACHE = CACHE_DIR / "tm-competition-rosters.json"
CACHE_TTL_SECONDS = 12 * 3600
TM_BASE = "https://tmapi-alpha.transfermarkt.technology"

# Те же восемь лиг, что на главной и в селекторе слухов: код Transfermarkt,
# id API-Football, название.
COMPETITIONS = [
    ("GB1", 39, "Premier League"),
    ("ES1", 140, "La Liga"),
    ("IT1", 135, "Serie A"),
    ("L1", 78, "Bundesliga"),
    ("FR1", 61, "Ligue 1"),
    ("TR1", 203, "Süper Lig"),
    ("PO1", 94, "Primeira Liga"),
    ("RU1", 235, "Russian Premier League"),
]

# Слова, ничего не говорящие о том, что это за клуб: у одного провайдера они
# есть, у другого нет. «Milan» и «AC Milan» — один клуб, «1.FC Köln» и «Köln»
# тоже.
NOISE = {
    "fc", "afc", "cf", "ac", "sc", "ss", "ssc", "us", "as", "sv", "vfb", "vfl",
    "tsg", "fsv", "bsc", "cd", "ud", "rc", "rcd", "sd", "sad", "sk", "club",
    "calcio", "futbol", "football", "futebol", "spor", "kulubu", "stade",
    "de", "of", "the", "1", "04", "05", "07", "96", "1846", "1899", "1900",
}

# Названия, которые не сходятся ни точно, ни по словам: другой язык, другая
# транслитерация, другое имя вовсе. Слева — как пишет Transfermarkt, справа —
# как записано у нас. Не данные, а синонимы: проверяется глазами один раз.
ALIASES = {
    "stade rennais": "rennes",
    "krylya sovetov samara": "krylia sovetov",
    "genclerbirligi ankara": "genclerbirligi",
    "deportivo a coruna": "deportivo la coruna",
    "sporting clube de portugal": "sporting cp",
    "sporting cp": "sporting cp",
}

# Турецкая «ı» и подобные буквы не раскладываются в NFD, и обычная чистка
# превращает «Kasımpaşa» в «kas mpasa». Раскладываем вручную.
TRANSLIT = str.maketrans({
    "ı": "i", "İ": "i", "ş": "s", "Ş": "s", "ğ": "g", "Ğ": "g",
    "ø": "o", "Ø": "o", "đ": "d", "Đ": "d", "ł": "l", "Ł": "l",
    "ß": "ss", "æ": "ae", "œ": "oe",
})


def normalize(value: str) -> str:
    text = str(value or "").translate(TRANSLIT)
    text = unicodedata.normalize("NFD", text)
    text = "".join(ch for ch in text if unicodedata.category(ch) != "Mn")
    text = text.lower().replace("&", " ").replace(".", " ").replace("-", " ")
    text = re.sub(r"[^a-z0-9 ]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return ALIASES.get(text, text)


def tokens(value: str) -> frozenset[str]:
    return frozenset(w for w in normalize(value).split() if w not in NOISE)


def tm_get(path: str, attempts: int = 3) -> dict:
    request = urllib.request.Request(TM_BASE + path, headers={
        "Accept": "application/json", "User-Agent": "promyachik/1.0"})
    last: Exception | None = None
    for attempt in range(attempts):
        try:
            with urllib.request.urlopen(
                    request, timeout=30,
                    context=ssl.create_default_context()) as response:
                return json.loads(response.read())
        except Exception as error:  # noqa: BLE001
            last = error
            time.sleep(1.5 * (attempt + 1))
    raise RuntimeError("Transfermarkt не ответил на %s: %s" % (path, last))


def load_cache() -> dict:
    """Состав лиги — это двадцать запросов; повторять их при каждом прогоне
    незачем, за полсуток он не меняется."""
    if not ROSTER_CACHE.exists():
        return {}
    try:
        cache = json.loads(ROSTER_CACHE.read_text(encoding="utf-8"))
    except Exception:  # noqa: BLE001
        return {}
    if time.time() - float(cache.get("saved_at") or 0) > CACHE_TTL_SECONDS:
        return {}
    return cache.get("rosters") or {}


def save_cache(rosters: dict) -> None:
    ROSTER_CACHE.parent.mkdir(parents=True, exist_ok=True)
    ROSTER_CACHE.write_text(
        json.dumps({"saved_at": time.time(), "rosters": rosters},
                   ensure_ascii=False, indent=1) + "\n",
        encoding="utf-8")


def competition_clubs(code: str) -> list[dict]:
    payload = tm_get("/competition/%s/table" % code)
    ids: list[str] = []
    for table in (payload.get("data") or {}).get("tables") or []:
        for row in table.get("clubs") or []:
            club_id = row.get("clubId")
            if club_id and str(club_id) not in ids:
                ids.append(str(club_id))

    clubs = []
    for club_id in ids:
        data = tm_get("/club/%s" % club_id).get("data") or {}
        base = data.get("baseDetails") or {}
        clubs.append({
            "tm_id": club_id,
            "name": data.get("name") or "",
            "short": base.get("shortName") or "",
        })
    return clubs


def match_club(tm_club: dict, directory: dict) -> list[str]:
    """Кандидаты из справочника API-Football. Пусто или больше одного — руками."""
    names = [n for n in (tm_club["name"], tm_club["short"]) if n]
    exact = {normalize(n) for n in names}

    hits = [club_id for club_id, club in directory.items()
            if any(normalize(v) in exact
                   for v in (club.get("name"), club.get("configured_name")) if v)]
    if len(hits) == 1:
        return hits

    # Вложение наборов значимых слов: «Brighton» ⊂ «Brighton & Hove Albion».
    tm_sets = [s for s in (tokens(n) for n in names) if s]
    loose: list[str] = []
    for club_id, club in directory.items():
        for variant in (club.get("name"), club.get("configured_name")):
            if not variant:
                continue
            api_set = tokens(variant)
            if api_set and any(s <= api_set or api_set <= s for s in tm_sets):
                if club_id not in loose:
                    loose.append(club_id)
                break
    return loose


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--save", action="store_true", help="записать изменения")
    args = parser.parse_args()

    directory = json.loads(CLUB_DIRECTORY.read_text(encoding="utf-8"))
    clubs = directory.get("clubs") or {}
    print("Клубов в справочнике: %d" % len(clubs))

    rosters = load_cache()
    for code, _league_id, league_name in COMPETITIONS:
        cached = code in rosters
        if not cached:
            try:
                rosters[code] = competition_clubs(code)
            except Exception as error:  # noqa: BLE001
                print("  ! %s (%s): %s" % (league_name, code, error))
                print("    без полного набора лиг файл не пишется")
                return 3
        print("  %-4s %-24s клубов: %d%s"
              % (code, league_name, len(rosters[code]),
                 "  (из кэша)" if cached else ""))
    save_cache(rosters)

    mapping: dict[str, int] = {}
    unmatched: list[str] = []
    ambiguous: list[str] = []

    for code, league_id, league_name in COMPETITIONS:
        for tm_club in rosters[code]:
            hits = match_club(tm_club, clubs)
            if len(hits) == 1:
                mapping[hits[0]] = league_id
            elif not hits:
                unmatched.append("%-24s %-24s (tm %s)"
                                 % (league_name, tm_club["name"], tm_club["tm_id"]))
            else:
                ambiguous.append("%-24s %-24s -> %s"
                                 % (league_name, tm_club["name"],
                                    ", ".join("%s %s" % (h, clubs[h].get("name"))
                                              for h in hits)))

    gained = [cid for cid in mapping if not clubs.get(cid, {}).get("league_id")]
    moved = [cid for cid, lid in mapping.items()
             if clubs.get(cid, {}).get("league_id")
             and clubs[cid]["league_id"] != lid]
    stale = [cid for cid, club in clubs.items()
             if club.get("league_id") and cid not in mapping]

    print("\nСведено клубов: %d из %d"
          % (len(mapping), sum(len(rosters[c]) for c, _, _ in COMPETITIONS)))

    print("\nПоявилась лига там, где её не было: %d" % len(gained))
    for cid in sorted(gained, key=lambda c: mapping[c]):
        print("  %-6s %-28s -> %s" % (cid, clubs[cid].get("name"), mapping[cid]))

    print("\nСменили лигу: %d" % len(moved))
    for cid in moved:
        print("  %-6s %-28s %s -> %s"
              % (cid, clubs[cid].get("name"), clubs[cid].get("league"), mapping[cid]))

    print("\nВ текущих составах нет, останутся с прошлой лигой: %d" % len(stale))
    for cid in stale:
        print("  %-6s %-28s %s" % (cid, clubs[cid].get("name"), clubs[cid].get("league")))

    if ambiguous:
        print("\nНеоднозначно, пропущено: %d" % len(ambiguous))
        for line in ambiguous:
            print("  " + line)
    if unmatched:
        print("\nВ лиге есть, в справочнике нет "
              "(движок дозакажет при первом трансфере): %d" % len(unmatched))
        for line in unmatched:
            print("  " + line)

    if not args.save:
        print("\nСухой прогон. Записать: --save")
        return 0

    OUTPUT.write_text(json.dumps({
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source": "transfermarkt open api, competition table текущего сезона",
        "note": ("id клуба API-Football -> id лиги API-Football. "
                 "Клуба здесь нет — шаблон берёт league_id из club-logos.json."),
        "clubs": {cid: mapping[cid] for cid in sorted(mapping, key=int)},
    }, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print("\nЗаписано: %s" % OUTPUT)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
