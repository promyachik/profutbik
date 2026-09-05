"""
PROMYACHIK TRANSFER AUTOPILOT - JOB BUILDER

Превращает обогащённого кандидата в job.json для замороженного движка 3.4.

Движок не переписывается: сборщик готовит ровно тот контракт, который
движок уже принимает, и который прошёл серию 5/5.

Правила, которые здесь соблюдаются жёстко:
  - ничего не выдумывается: нет данных -> кандидат уходит в NEEDS_REVIEW;
  - API-Football id клубов берётся из моста, при отсутствии - точный lookup
    по ключу, без угадывания числа;
  - поле fee короткое, без атрибуции в скобках (она идёт вниз статьи);
  - точки графика только реальные чекпоинты Transfermarkt.

Ничего не публикует и не изменяет Promyachik_CLEAN.
"""
from __future__ import annotations

import argparse
import json
import re
import ssl
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from transfer_discovery import (  # noqa: E402
    ACTIVE_PROJECT, PARSER_ROOT, RECORDS_DIR, normalize, slugify,
)
from transfer_enrichment import build_tm_club_index, resolve_tm_club  # noqa: E402
from reference_bridge import (  # noqa: E402
    POSITIONS, load_club_bridge, load_country_map,
)

JOBS_DIR = PARSER_ROOT / "jobs"
MONTHS_RU = ["января", "февраля", "марта", "апреля", "мая", "июня",
             "июля", "августа", "сентября", "октября", "ноября", "декабря"]

FOOT_RU = {"right": "Правая", "left": "Левая", "both": "Обе"}


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def ru_date(iso: str) -> str:
    try:
        parsed = datetime.strptime(iso[:10], "%Y-%m-%d")
    except Exception:
        return iso
    return "%d %s %d года" % (parsed.day, MONTHS_RU[parsed.month - 1], parsed.year)


def dotted_date(iso: str) -> str:
    try:
        return datetime.strptime(iso[:10], "%Y-%m-%d").strftime("%d.%m.%Y")
    except Exception:
        return ""


def money_ru(value: str) -> str:
    """'£51m' -> '£51 млн'. Ничего не пересчитываем между валютами."""
    if not value:
        return ""
    match = re.match(r"([\u00a3\u20ac$])\s?([\d.,]+)\s?(m|bn)?", value.strip(), re.I)
    if not match:
        return value.strip()
    symbol, amount, scale = match.groups()
    amount = amount.rstrip(".,").replace(".", ",")
    suffix = {"m": " млн", "bn": " млрд"}.get((scale or "m").lower(), " млн")
    return "%s%s%s" % (symbol, amount, suffix)


# ---------------------------------------------------------------------------
# API-Football: точный lookup, когда моста нет
# ---------------------------------------------------------------------------

# Молодёжные и женские команды в выдаче API-Football: их брать нельзя.
# Границы слов обязательны: без них одиночная W совпадала внутри
# Newcastle и отсекала нормальные клубы.
YOUTH_OR_WOMEN = re.compile(
    r"\b(?:U-?\d{2}|W|Women|Womens|Youth|Academy|Reserves|II)\b", re.I)


def api_football_key() -> str | None:
    import os
    # В облаке ключ приходит переменной окружения: репозиторий
    # публичный, файлам с секретами там не место.
    direct = os.environ.get("API_FOOTBALL_KEY")
    if direct:
        return direct.strip()
    from paths import ENV_FILES
    for path in ENV_FILES:
        if not path.exists():
            continue
        for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
            match = re.match(r"\s*API_FOOTBALL_KEY\s*=\s*(.+)", line)
            if match:
                return match.group(1).strip().strip("\"'")
    return None


class ApiFootballQuotaExceeded(RuntimeError):
    """Дневной лимит API-Football исчерпан.

    Отдельное исключение нужно, чтобы не путать «клуб не найден» с
    «нас не пустили»: раньше и то и другое возвращало None, и клуб молча
    оставался без логотипа, хотя он прекрасно существует.
    """


def _api_football_search(query: str, key: str) -> list[dict]:
    url = "https://v3.football.api-sports.io/teams?search=%s" % urllib.parse.quote(query)
    request = urllib.request.Request(url, headers={
        "x-apisports-key": key, "Accept": "application/json"})
    try:
        with urllib.request.urlopen(
                request, timeout=25, context=ssl.create_default_context()) as response:
            payload = json.loads(response.read())
    except urllib.error.HTTPError as error:
        if error.code == 429:
            raise ApiFootballQuotaExceeded(
                "дневной лимит API-Football исчерпан") from error
        return []
    except Exception:
        return []

    # Лимит может прийти и как 200 с сообщением в errors.
    errors = payload.get("errors")
    if isinstance(errors, dict) and any(
            "limit" in str(v).lower() or "quota" in str(v).lower()
            for v in errors.values()):
        raise ApiFootballQuotaExceeded(str(errors))
    return payload.get("response", []) or []


def api_football_lookup(club_name: str, country_hint: str = "") -> int | None:
    """Разрешение клуба по названию. id возвращается только при однозначности.

    country_hint обязателен для одноимённых клубов: "Newcastle" существует
    и в Англии, и в Северной Ирландии.
    """
    key = api_football_key()
    if not key:
        return None

    from transfer_enrichment import club_tokens

    rows = _api_football_search(club_name, key)
    wanted = normalize(club_name)
    wanted_tokens = club_tokens(club_name)

    # API-Football часто хранит короткое имя: по запросу "Coventry City"
    # приходят только молодёжные составы, а взрослая команда зовётся
    # "Coventry". Пробуем ещё раз по самому длинному значимому слову.
    if not rows or all(YOUTH_OR_WOMEN.search(r.get("team", {}).get("name") or "")
                       for r in rows):
        # Берём ПЕРВОЕ значимое слово, а не самое длинное: у "Leeds United"
        # длиннее "united", но различает клуб именно "Leeds".
        parts = [p for p in normalize(club_name).split()
                 if p in wanted_tokens]
        short = parts[0] if parts else ""
        if short and short != wanted:
            rows = _api_football_search(short, key) or rows

    payload = {"response": rows}
    exact: list[int] = []
    loose: list[int] = []

    for row in payload.get("response", []):
        team = row.get("team") or {}
        name = team.get("name") or ""
        if team.get("national") or not name:
            continue
        # Молодёжные и женские команды - не тот клуб.
        if YOUTH_OR_WOMEN.search(name):
            continue
        if country_hint and normalize(team.get("country", "")) != normalize(country_hint):
            continue

        if normalize(name) == wanted:
            exact.append(team["id"])
            continue
        # API-Football зовёт клубы короче: "Coventry" против "Coventry City".
        # Значимые слова одного должны целиком входить в другой, иначе это
        # другой клуб ("Coventry United" под "Coventry City" не подходит).
        have = club_tokens(name)
        if have and wanted_tokens and (have <= wanted_tokens or wanted_tokens <= have):
            loose.append(team["id"])

    if len(exact) == 1:
        return exact[0]
    if not exact and len(loose) == 1:
        return loose[0]
    return None


# ---------------------------------------------------------------------------

def resolve_api_id(club_name: str, tm_clubs: dict, bridge: dict,
                   allow_network: bool) -> tuple[int | None, str]:
    tm_id = resolve_tm_club(club_name, tm_clubs)
    if tm_id and str(tm_id) in bridge:
        return bridge[str(tm_id)]["api_football_id"], "bridge"
    if allow_network:
        found = api_football_lookup(club_name)
        if found:
            return found, "api_lookup"
    return None, "unresolved"


def euro(value: float) -> str:
    return "€%s млн" % ("%g" % value).replace(".", ",")


# Transfermarkt отдаёт величину суффиксом: "B" (не "BN"), "M", "K".
SCALE_RU = {"b": "млрд", "bn": "млрд", "m": "млн", "k": "тыс."}


def compact_money(compact: dict) -> str:
    """{'prefix':'€','content':'1.29','suffix':'B'} -> '€1,29 млрд'.

    Умолчания здесь нет намеренно. Раньше неизвестный суффикс подставлял
    "млн", и стоимость состава Barcelona выводилась как €1,29 млн вместо
    €1,29 млрд. Неизвестный суффикс -> пустая строка, факт просто не пишем:
    лучше промолчать, чем ошибиться на три порядка.
    """
    if not compact or not compact.get("content"):
        return ""
    suffix = str(compact.get("suffix") or "").strip().lower()
    scale = SCALE_RU.get(suffix)
    if not scale:
        return ""
    return "%s%s %s" % (compact.get("prefix") or "€",
                        str(compact["content"]).replace(".", ","), scale)


def plural_ru(count: int, one: str, few: str, many: str) -> str:
    """Согласование числительного: 1 игрок, 2 игрока, 5 игроков."""
    tail_100 = count % 100
    tail_10 = count % 10
    if 11 <= tail_100 <= 14:
        return many
    if tail_10 == 1:
        return one
    if 2 <= tail_10 <= 4:
        return few
    return many


def parse_former_clubs(note: str) -> list[tuple[str, str]]:
    """'LOSC Lille (2014-2020), KAA Gent (2020-2022)' -> [(клуб, годы), ...]"""
    result = []
    for chunk in re.split(r",\s*(?![^()]*\))", note or ""):
        match = re.match(r"\s*(.+?)\s*\(([^)]+)\)\s*$", chunk)
        if match:
            result.append((match.group(1).strip(), match.group(2).strip()))
    return result


# Стилевые регистры. Выбор детерминирован по entity_id: один и тот же игрок
# всегда получает один и тот же стиль, но у разных игроков стили разные.
STYLES = ("business", "analytic", "narrative")


def pick_style(entity_id: str) -> str:
    digest = sum(ord(ch) for ch in entity_id)
    return STYLES[digest % len(STYLES)]


# Латинское название клуба в русском тексте не склоняется и своего рода
# не имеет: "Barcelona усилил" и "Barcelona усилила" одинаково неверны.
# Поэтому склоняем слово "клуб", а название оставляем неизменным.
CLUB_CASES = {"nom": "клуб", "gen": "клуба", "dat": "клубу",
              "acc": "клуб", "ins": "клубом", "prep": "клубе"}


def club_word(name: str, case: str = "nom", capitalize: bool = False) -> str:
    """"клуб Barcelona", "клуба Barcelona", "клубе Barcelona" и т.д."""
    word = CLUB_CASES.get(case, "клуб")
    if capitalize:
        word = word[0].upper() + word[1:]
    return "%s %s" % (word, name)


def club_subject(name: str, capitalize: bool = False) -> str:
    """Клуб как подлежащее - именительный падеж."""
    return club_word(name, "nom", capitalize)


def block_lead(style: str, player: str, to_club: str, from_club: str,
               date_ru: str, fee_ru: str, position_ru: str, age) -> list[str]:
    if style == "business":
        text = "%s объявил о подписании **%s**." % (
            club_subject("**%s**" % to_club, capitalize=True), player)
        if from_club:
            text += " %s перешёл из %s." % (
                "Игрок" if not position_ru else position_ru,
                club_word("**%s**" % from_club, "gen"))
        if date_ru:
            text += " Сделка оформлена **%s**." % date_ru
        if fee_ru:
            text += " Сумма трансфера — **%s**." % fee_ru
    elif style == "analytic":
        text = "%s усилил состав и подписал **%s**" % (
            club_subject("**%s**" % to_club, capitalize=True), player)
        if from_club:
            text += " из %s" % club_word("**%s**" % from_club, "gen")
        text += "."
        if fee_ru:
            text += " Стоимость перехода составила **%s**." % fee_ru
        if date_ru:
            text += " Переход оформлен **%s**." % date_ru
    else:
        who = position_ru.lower() if position_ru else "футболист"
        text = "**%s** — %s" % (player, who)
        if age:
            text += ", которому %d" % age
        text += " — продолжит карьеру в %s" % club_word(
            "**%s**" % to_club, "prep")
        if from_club:
            text += ", покинув **%s**" % from_club
        text += "."
        if date_ru:
            text += " Переход состоялся **%s**." % date_ru
        if fee_ru:
            text += " Клуб заплатил за него **%s**." % fee_ru
    return [text]


def block_career(style: str, player: str, record: dict, country_ru: str) -> list[str]:
    former = parse_former_clubs(record.get("former_clubs_note") or "")
    birth_place = record.get("birth_place") or ""
    if not former and not birth_place:
        return []

    parts = []
    name_short = player.split()[-1]
    if birth_place:
        first = "%s родился в городе %s" % (player, birth_place)
        if country_ru:
            first += " (%s)" % country_ru
        first += "."
        parts.append(first)
    if former:
        clubs = ", ".join("%s (%s)" % (club, years) for club, years in former)
        if style == "narrative":
            parts.append("Путь игрока до нынешнего перехода: %s." % clubs)
        else:
            parts.append("Ранее выступал за: %s." % clubs)
        if len(former) >= 3:
            parts.append(
                "Таким образом, это уже %d-й клуб в карьере %s."
                % (len(former) + 1, name_short))
    return [" ".join(parts)] if parts else []


def block_market(style: str, player: str, points: list[dict],
                 fee_ru: str, fee_raw: str) -> list[str]:
    if not points:
        return []
    name_short = player.split()[-1]
    current = points[-1]["value_eur_m"]
    peak = max(p["value_eur_m"] for p in points)
    parts = []

    if len(points) >= 2:
        first = points[0]
        change = current - first["value_eur_m"]
        direction = "выросла" if change > 0 else ("снизилась" if change < 0 else "не изменилась")
        parts.append(
            "По оценке Transfermarkt с %s по %s стоимость %s %s с %s до %s."
            % (ru_date(first["date"]), ru_date(points[-1]["date"]), name_short,
               direction, euro(first["value_eur_m"]), euro(current)))
    else:
        parts.append("Текущая оценка Transfermarkt — %s (%s)."
                     % (euro(current), ru_date(points[-1]["date"])))

    if peak > current:
        parts.append("Максимальная оценка за этот период — %s." % euro(peak))

    # Сравнение суммы с оценкой корректно только в одной валюте.
    if fee_raw.strip().startswith("€"):
        fee_value = re.match(r"€\s?([\d.,]+)", fee_raw.strip())
        if fee_value:
            try:
                amount = float(fee_value.group(1).replace(",", "."))
                if amount > current:
                    parts.append(
                        "Сумма сделки выше текущей оценки игрока на %s."
                        % euro(round(amount - current, 2)))
                elif amount < current:
                    parts.append(
                        "Клуб заплатил на %s меньше рыночной оценки."
                        % euro(round(current - amount, 2)))
            except ValueError:
                pass
    elif fee_ru:
        parts.append(
            "Рыночная оценка и сумма сделки указаны в разных валютах, "
            "поэтому напрямую они не сопоставляются.")
    return [" ".join(parts)]


def block_destination(style: str, player: str, to_club: str,
                      record: dict) -> list[str]:
    context = record.get("to_club_context") or {}
    if not context:
        return []
    parts = []
    size = context.get("squad_size")
    age = context.get("average_age")
    value = context.get("squad_value") or {}
    average = context.get("average_player_value") or {}
    stadium = context.get("stadium")
    city = context.get("city")

    # Размер состава берём из фактического списка игроков: club API иногда
    # даёт другое число, и в одном тексте появлялись сразу 26 и 27.
    analysis = record.get("squad_analysis") or {}
    size = analysis.get("squad_total") or size
    if size and age:
        count = int(size)
        parts.append("В составе %s теперь %d %s со средним возрастом %s года."
                     % (club_word(to_club, "gen"), count,
                        plural_ru(count, "игрок", "игрока", "игроков"),
                        str(age).replace(".", ",")))
    squad_value = compact_money(value)
    if squad_value:
        line = "Общая стоимость команды по Transfermarkt — %s" % squad_value
        average_value = compact_money(average)
        if average_value:
            line += ", в среднем %s на игрока" % average_value
        parts.append(line + ".")
    if city:
        # В поле street у части клубов лежит адрес, а не название стадиона,
        # поэтому стадион не называем - только город.
        parts.append("Домашние матчи команда проводит в городе %s."
                     % city.strip())

    number = record.get("shirt_number")
    if number:
        parts.append("В новой команде игрок получил %d-й номер." % int(number))
    return [" ".join(parts)] if parts else []


def block_competition(style: str, player: str, position_ru: str,
                      record: dict) -> list[str]:
    """Конкуренция за позицию и место игрока в составе.

    Считается из уже загруженного состава клуба назначения: никаких
    дополнительных запросов и никаких оценочных суждений - только счёт.
    """
    analysis = record.get("squad_analysis") or {}
    if not analysis:
        return []
    parts = []

    rivals = analysis.get("same_position_count") or 0
    names = analysis.get("same_position_names") or []
    if rivals:
        if rivals == 1:
            parts.append("На этой же позиции в клубе значится ещё один игрок — %s."
                         % names[0])
        else:
            listed = ", ".join(names)
            parts.append(
                "Конкуренцию на этой позиции составят ещё %d %s: %s."
                % (rivals, plural_ru(rivals, "игрок", "игрока", "игроков"), listed))
    elif position_ru:
        parts.append("Других игроков этого амплуа в заявке клуба нет.")

    rank = analysis.get("value_rank")
    total = analysis.get("squad_total")
    if rank and total:
        if rank <= 3:
            parts.append(
                "По оценке Transfermarkt это %d-й по стоимости игрок команды из %d."
                % (rank, total))
        else:
            parts.append(
                "В рейтинге стоимости состава он занимает %d-е место из %d."
                % (rank, total))

    younger = analysis.get("younger_than") or 0
    age = record.get("age")
    if younger and age and total:
        parts.append("В свои %d %s он моложе %d %s команды."
                     % (age, plural_ru(age, "год", "года", "лет"), younger,
                        plural_ru(younger, "партнёра", "партнёров", "партнёров")))
    return [" ".join(parts)] if parts else []


# Названия стран по-русски склоняются, в отличие от латинских названий
# клубов. Правила покрывают основную массу, исключения заданы явно.
COUNTRY_GENITIVE = {
    "Босния и Герцеговина": "Боснии и Герцеговины",
    "Северная Ирландия": "Северной Ирландии",
    "Кот-д’Ивуар": "Кот-д’Ивуара",
    "Кот-д'Ивуар": "Кот-д'Ивуара",
    "Уэльс": "Уэльса",
    "США": "США",
    # Беглая гласная: Египет -> Египта, а не "Египета".
    "Египет": "Египта",
    "Кипр": "Кипра",
    "Азербайджан": "Азербайджана",
    "Конго": "Конго",
    "Перу": "Перу",
    "Чили": "Чили",
    "Гаити": "Гаити",
}


def country_genitive(name: str) -> str:
    """"Бельгия" -> "Бельгии", "Камерун" -> "Камеруна"."""
    if not name:
        return ""
    if name in COUNTRY_GENITIVE:
        return COUNTRY_GENITIVE[name]
    if name.endswith("ия"):
        return name[:-2] + "ии"
    if name.endswith("я"):
        return name[:-1] + "и"
    if name.endswith("а"):
        # После шипящих и заднеязычных пишется "и", иначе "ы".
        return name[:-1] + ("и" if name[-2] in "гкхжчшщ" else "ы")
    if name.endswith("й"):
        return name[:-1] + "я"
    if name.endswith(("ь",)):
        return name[:-1] + "я"
    return name + "а"


def block_national(player: str, record: dict, country_ru: str) -> list[str]:
    debut = record.get("national_team_debut")
    if not debut or not country_ru:
        return []
    return ["За сборную %s игрок дебютировал %s."
            % (country_genitive(country_ru), ru_date(debut))]


def build_body(record: dict, fee_ru: str, position_ru: str,
               country_ru: str) -> str:
    player = record["player_full_name"]
    to_club = record["to_club"]
    from_club = record["from_club"] or ""
    style = pick_style(record.get("entity_id") or player)
    date_ru = ru_date(record.get("transfer_date")
                      or (record.get("source") or {}).get("published_iso") or "")
    points = record.get("market_value_points") or []
    market = euro(points[-1]["value_eur_m"]) if points else ""

    headings = {
        "business": ("%s переходит в %s" % (player, to_club),
                     "Детали перехода", "Что получает клуб", "Карточка игрока"),
        "analytic": ("%s: что известно о переходе в %s" % (player, to_club),
                     "Динамика стоимости", "Клуб назначения", "Данные игрока"),
        "narrative": ("%s стал игроком %s" % (player, to_club),
                      "Карьера до перехода", "Новый клуб", "Профиль игрока"),
    }
    title, h2, h3, h4 = headings[style]

    lines = ["## %s" % title, ""]
    lines += block_lead(style, player, to_club, from_club, date_ru, fee_ru,
                        position_ru, record.get("age"))

    career = block_career(style, player, record, country_ru)
    market_block = block_market(style, player, points, fee_ru,
                                record.get("fee_raw") or "")
    national = block_national(player, record, country_ru)
    destination = block_destination(style, player, to_club, record)
    competition = block_competition(style, player, position_ru, record)

    middle = career + national if style == "narrative" else market_block
    tail = market_block if style == "narrative" else career + national

    def paragraphs(blocks: list[str]) -> list[str]:
        out: list[str] = []
        for block in blocks:
            if out:
                out.append("")
            out.append(block)
        return out

    if middle:
        lines += ["", "## %s" % h2, ""] + paragraphs(middle)
    if destination or competition or tail:
        lines += ["", "## %s" % h3, ""] + paragraphs(
            destination + competition + tail)

    facts = []
    if position_ru:
        facts.append("**Позиция:** %s" % position_ru.lower())
    if from_club:
        facts.append("**Прежний клуб:** %s" % from_club)
    facts.append("**Новый клуб:** %s" % to_club)
    if country_ru:
        facts.append("**Гражданство:** %s" % country_ru)
    if record.get("birth_date"):
        facts.append("**Дата рождения:** %s" % dotted_date(record["birth_date"]))
    if record.get("birth_place"):
        facts.append("**Место рождения:** %s" % record["birth_place"])
    if record.get("height"):
        facts.append("**Рост:** %s м" % str(record["height"]).replace(".", ","))
    foot = FOOT_RU.get((record.get("preferred_foot") or "").lower())
    if foot:
        facts.append("**Рабочая нога:** %s" % foot.lower())
    if record.get("shirt_number"):
        facts.append("**Игровой номер:** %d" % int(record["shirt_number"]))
    if market:
        facts.append("**Рыночная стоимость Transfermarkt:** %s" % market)
    if fee_ru:
        facts.append("**Сумма трансфера:** %s" % fee_ru)
    if record.get("contract_until"):
        facts.append("**Контракт до:** %s" % dotted_date(record["contract_until"]))
    facts.append("**Статус:** официальный переход")

    lines += ["", "## %s" % h4, ""] + ["- %s" % fact for fact in facts]

    source = record.get("source") or {}
    if source.get("publisher"):
        lines += ["", "---", "",
                  "**Источник:** %s. Данные игрока и рыночная стоимость — "
                  "Transfermarkt." % source["publisher"]]
    return "\n".join(lines)


def build_job(record: dict, tm_clubs: dict, bridge: dict, countries: dict,
              allow_network: bool) -> tuple[dict | None, str]:
    if record.get("pipeline_state") != "ENRICHED":
        return None, "кандидат не обогащён (%s)" % record.get("pipeline_state")

    player = record["player_full_name"]
    to_club = record["to_club"]
    from_club = record["from_club"]
    if not from_club:
        return None, "не определён прежний клуб"

    position_en = record.get("position") or ""
    position_ru, position_short = POSITIONS.get(position_en, ("", ""))
    if not position_ru:
        return None, "позиция %r не переведена" % position_en

    nationalities = record.get("nationality_ids") or {}
    country = countries.get(str(nationalities.get("nationalityId") or ""))
    if not country:
        return None, "гражданство id=%s отсутствует в справочнике" % (
            nationalities.get("nationalityId"))
    if not country.get("fifa_code"):
        return None, "нет кода ФИФА для страны %r" % country["name"]

    to_api, to_how = resolve_api_id(to_club, tm_clubs, bridge, allow_network)
    from_api, from_how = resolve_api_id(from_club, tm_clubs, bridge, allow_network)
    if not to_api:
        return None, "API-Football id клуба назначения %r не определён" % to_club
    if not from_api:
        return None, "API-Football id прежнего клуба %r не определён" % from_club

    fee_ru = money_ru(record.get("fee_raw") or "")
    slug = "%s-%s" % (slugify(player), slugify(to_club))
    flag = country["flag_code"]
    date_iso = (record.get("transfer_date")
                or (record.get("source") or {}).get("published_iso") or "")

    title = "%s перешёл из %s в %s" % (player, from_club, to_club)
    description = "%s подписал %s из %s." % (
        club_subject(to_club, capitalize=True), player,
        club_word(from_club, "gen"))
    if fee_ru:
        description += " Сумма трансфера составила %s." % fee_ru

    points = record.get("market_value_points") or []
    market = ("€%s млн" % ("%g" % points[-1]["value_eur_m"]).replace(".", ",")
              ) if points else ""

    job = {
        "slug": slug,
        "player": player,
        "full_name": player,
        "transfermarkt_player_id": int(record["tm_player_id"]),
        "transfermarkt_profile_url":
            "https://www.transfermarkt.com/-/profil/spieler/%s" % record["tm_player_id"],
        "transfermarkt_data_profile_url":
            "https://tmapi-alpha.transfermarkt.technology/player/%s" % record["tm_player_id"],
        "photo_required": True,
        "on_photo_missing": "block_without_site_publish",
        "batch_continue_after_photo_block": False,
        "from_club_id": int(from_api),
        "from_club_name": from_club,
        "to_club_id": int(to_api),
        "to_club_name": to_club,
        "title": title,
        "description": description,
        "status": "official",
        "status_label": "ОФИЦИАЛЬНО",
        "fee": fee_ru or "Сумма не разглашается",
        "draft": False,
        "test_mode": False,
        "position": position_en,
        "position_ru": position_ru,
        "main_position": record.get("position_short") or position_short,
        "birth_date": dotted_date(record.get("birth_date") or ""),
        "age": record.get("age"),
        "nationality": country["name"],
        "nationality_ru": country["name_ru"],
        "nationality_code": flag.upper(),
        "nationality_fifa_code": country["fifa_code"],
        "nationality_flag_aliases": sorted({
            country["name"], country["name"].lower(), flag, flag.upper(),
            country["fifa_code"], country["fifa_code"].lower(),
            "flag-%s" % flag,
        }),
        "preferred_foot": FOOT_RU.get((record.get("preferred_foot") or "").lower(), ""),
        "market_value": market,
        "market_value_display": market,
        "seo_body_md": build_body(record, fee_ru, position_ru, country["name_ru"]),
        "source_name": (record.get("source") or {}).get("publisher") or "",
        "source_status": "official_permanent_transfer",
        "source_url": (record.get("source") or {}).get("url") or "",
        "pipeline_engine_version": "3.4",
        "enabled_modules": ["homepage_transfer", "upper_ticker",
                            "lower_ticker", "player_page"],
        "input_mode": "fresh_verified_transfer_news",
        "fresh_news_parse": {
            "source_published_date": date_iso[:10],
            "effective_transfer_date": date_iso[:10],
            "parser_result": "official_permanent_transfer",
            "player": player,
            "from_club": from_club,
            "to_club": to_club,
            "status": "official",
            "fee": record.get("fee_raw") or "not_disclosed",
            "not_from_existing_site_database": True,
        },
        "club_logo_policy": {
            "mode": "on_demand_cache",
            "download_missing_known_api_id_clubs": True,
            "do_not_bulk_download_entire_leagues": True,
            "historical_graph_clubs_included": True,
            "verified_api_ids": {from_club: int(from_api), to_club: int(to_api)},
        },
        "package_intent": "autopilot_full_1_2_3_4_plus_lower_ticker",
        "_autopilot": {
            "entity_id": record["entity_id"],
            "built_at": now_iso(),
            "api_id_resolution": {"from": from_how, "to": to_how},
            "market_value_points": points,
        },
    }
    return job, ""


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Promyachik job builder")
    parser.add_argument("--save", action="store_true",
                        help="записать job.json в parser/jobs")
    parser.add_argument("--network", action="store_true",
                        help="разрешить lookup API-Football для клубов без моста")
    args = parser.parse_args(argv)

    tm_clubs = build_tm_club_index(verbose=False)
    bridge = load_club_bridge()
    countries = load_country_map()
    print("\n=== СБОРКА JOB (сайт не изменялся) ===")
    print("  мост клубов: %d | стран: %d" % (len(bridge), len(countries)))

    JOBS_DIR.mkdir(parents=True, exist_ok=True)
    built, failed = 0, 0
    for path in sorted(RECORDS_DIR.glob("*.json")):
        try:
            record = json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            continue
        if record.get("schema_version") != 2 or record.get("pipeline_state") != "ENRICHED":
            continue

        job, reason = build_job(record, tm_clubs, bridge, countries, args.network)
        if not job:
            failed += 1
            print("\n  [NEEDS_REVIEW] %s : %s" % (record.get("player"), reason))
            continue

        built += 1
        print("\n  [ГОТОВ] %s" % job["slug"])
        print("     %s (TM %s)" % (job["player"], job["transfermarkt_player_id"]))
        print("     %s (%s) -> %s (%s)" % (
            job["from_club_name"], job["from_club_id"],
            job["to_club_name"], job["to_club_id"]))
        print("     %s | %s | %s | fee: %s" % (
            job["position_ru"], job["nationality_ru"], job["birth_date"], job["fee"]))
        print("     текст: %d слов | точек графика: %d" % (
            len(re.findall(r"\w+", job["seo_body_md"])),
            len(job["_autopilot"]["market_value_points"])))
        if args.save:
            out = JOBS_DIR / ("autopilot_%s.json" % job["slug"])
            out.write_text(json.dumps(job, ensure_ascii=False, indent=2) + "\n",
                           encoding="utf-8")
            print("     -> %s" % out)

    print("\n  собрано: %d | требуют разбора: %d\n" % (built, failed))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
