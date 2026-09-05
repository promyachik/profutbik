"""
PROMYACHIK TRANSFER AUTOPILOT - ПУБЛИКАЦИЯ СЛУХОВ

Договорённость, которая ещё не стала переходом, публикуется в раздел
"Слухи" со своей страницей, своим SEO и своим статусом.

Как потом слух превращается в трансфер:

    Из слухов ничего не "вытаскивается" сканированием сайта.
    Запись в очереди парсера живёт независимо от того, где лежит контент,
    и хранит entity_id. Каждый прогон перепроверяет все записи в состоянии
    PUBLISHED_AS_RUMOR через состав клуба назначения. Как только игрок там
    появился, сделка считается закрытой: выходит полноценный трансфер,
    страница слуха удаляется, а со старого адреса ставится редирект.

    Сайт - это вывод. Состояние живёт в очереди.

Slug намеренно НЕ содержит статуса: адрес не должен меняться при переходе
по лестнице rumour -> negotiations -> agreement.
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
import unicodedata
from datetime import datetime, timezone
from pathlib import Path

BIN = Path(__file__).resolve().parent
sys.path.insert(0, str(BIN))
from transfer_discovery import ACTIVE_PROJECT, PARSER_ROOT, RECORDS_DIR, slugify  # noqa: E402
from transfer_enrichment import build_tm_club_index  # noqa: E402
from reference_bridge import load_club_bridge, load_country_map, POSITIONS  # noqa: E402
from job_builder import (  # noqa: E402
    club_word, country_genitive, dotted_date, euro, money_ru,
    parse_former_clubs, resolve_api_id, ru_date,
)

RUMORS_DIR = ACTIVE_PROJECT / "content" / "rumors"
HOMEPAGE_JSON = ACTIVE_PROJECT / "data" / "homepage_transfer_rumor.json"
CLUB_LOGOS = ACTIVE_PROJECT / "data" / "club-logos.json"

# Лестница статусов, которую уже понимает сайт.
STATUS_LABELS = {
    "rumour": ("СЛУХ", "слух", "is-rumor"),
    "negotiations": ("ПЕРЕГОВОРЫ", "переговоры", "is-talks"),
    "agreement": ("СОГЛАСОВАНО", "согласовано", "is-agreement"),
}

# Ниже этого объёма слух не публикуется. Цифра не с потолка: у страниц
# трансферов медиана 165 слов, и они уже на грани; для материала, который
# конкурирует с BBC и Sky по тому же запросу, 300 — минимум приличия.
MIN_RUMOR_WORDS = 300

LEAGUE_BY_COUNTRY = {
    "England": ("39", "Premier League"), "Spain": ("140", "La Liga"),
    "Italy": ("135", "Serie A"), "Germany": ("78", "Bundesliga"),
    "France": ("61", "Ligue 1"), "Portugal": ("94", "Primeira Liga"),
    "Netherlands": ("88", "Eredivisie"), "Turkey": ("203", "Super Lig"),
    "Russia": ("235", "Premier Liga"), "Saudi-Arabia": ("307", "Saudi Pro League"),
}


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def club_entry(api_id: int) -> dict:
    catalog = json.loads(CLUB_LOGOS.read_text(encoding="utf-8"))
    clubs = catalog.get("clubs", catalog)
    return (clubs or {}).get(str(api_id)) or {}


def rumor_slug(record: dict) -> str:
    """Стабильный адрес без статуса: он не меняется по мере развития сюжета."""
    name = record.get("player_full_name") or record.get("player") or ""
    return "%s-%s" % (slugify(name), slugify(record.get("to_club") or ""))


CLUB_LINKS = ACTIVE_PROJECT / "data" / "club_links.json"


def club_link(api_id, name: str) -> str:
    """Название клуба ссылкой на его страницу, если она у нас есть.

    До этого страницы слухов не имели ни одной внутренней ссылки — ни на
    клубы, ни на трансферы. Для поиска это тупик: вес некуда передавать, а
    человеку некуда идти дальше. Клубных страниц у нас 148, связываем по
    числовому id, а не по названию: «Atlético de Madrid» на странице клуба и
    «Atletico Madrid» в слухе — один клуб, но разные строки.
    """
    if not api_id:
        return name
    try:
        links = json.loads(CLUB_LINKS.read_text(encoding="utf-8"))
    except Exception:
        return name
    url = (links.get(str(api_id)) or {}).get("url")
    return "[%s](%s)" % (name, url) if url else name


def value_story(points: list) -> str:
    """Что говорит история оценок Transfermarkt.

    Единственный раздел, которого у конкурентов в слухах нет: там пересказ
    чужого сообщения и всё. Оценки мы храним для графика, поэтому разбор
    ничего не стоит и опирается на числа, а не на предположения.
    """
    if not points:
        return ""
    current, first = points[-1], points[0]
    peak = max(points, key=lambda item: item.get("value_eur_m") or 0)
    parts = ["Сейчас Transfermarkt оценивает игрока в **%s**."
             % euro(current["value_eur_m"])]

    if (peak.get("value_eur_m") or 0) > (current.get("value_eur_m") or 0):
        delta = peak["value_eur_m"] - current["value_eur_m"]
        share = round(100 * delta / peak["value_eur_m"])
        parts.append(
            "Пик пришёлся на %s, тогда он стоил %s: с того момента оценка "
            "снизилась на %s, то есть на %d%% от максимума."
            % (ru_date(peak["date"]), euro(peak["value_eur_m"]),
               euro(delta), share))
    elif (current.get("value_eur_m") or 0) > (first.get("value_eur_m") or 0):
        growth = round(100 * (current["value_eur_m"] - first["value_eur_m"])
                       / max(first["value_eur_m"], 0.1))
        parts.append(
            "Это максимум карьеры: с первой оценки в %s от %s стоимость "
            "выросла на %d%%."
            % (euro(first["value_eur_m"]), ru_date(first["date"]), growth))

    if len(points) >= 3:
        parts.append("Всего у игрока %d переоценок, первая — %s."
                     % (len(points), ru_date(first["date"])))
    return " ".join(parts)


def tm_money(value: dict) -> str:
    """Сумма из Transfermarkt в человеческий вид.

    Суффикс у них «B», а не «BN», и на этом мы уже обжигались: умолчание в
    таблице масштабов превращало 1,29 млрд в 1,29 млн. Неизвестный суффикс —
    факт не печатаем вовсе.
    """
    if not isinstance(value, dict):
        return ""
    scale = {"B": "млрд", "M": "млн", "K": "тыс."}.get(
        str(value.get("suffix") or "").upper())
    content = str(value.get("content") or "").strip()
    if not scale or not content:
        return ""
    return "%s%s %s" % (value.get("prefix") or "€", content.replace(".", ","), scale)


def competition_story(record: dict, position_ru: str, to_club: str) -> str:
    """Кто уже играет на этой позиции в клубе назначения.

    Ради этого раздела всё и затевалось: у конкурентов в слухах пересказ
    сообщения, а здесь видно, зачем клубу игрок и с кем он будет спорить за
    место. Данные лежат в записи с обогащения, считать заново ничего не надо.
    """
    analysis = record.get("squad_analysis") or {}
    same = analysis.get("same_position_count")
    names = analysis.get("same_position_names") or []
    total = analysis.get("squad_total")
    younger = analysis.get("younger_than")
    if same is None and not total:
        return ""

    parts = []
    if same == 0:
        parts.append("Чистого конкурента на этой позиции в составе %s сейчас нет."
                     % to_club)
    elif same:
        who = ", ".join(names[:3])
        word = "игрок" if same == 1 else ("игрока" if same < 5 else "игроков")
        parts.append("На этой позиции в клубе уже %d %s%s."
                     % (same, word, (" — %s" % who) if who else ""))
    if total:
        parts.append("Всего в заявке %d футболистов." % total)
    if younger and total:
        parts.append("Он моложе %d из %d футболистов заявки." % (younger, total))
    return " ".join(parts)


def club_portrait(record: dict, to_club: str, league: str) -> str:
    """Что за команда: размер заявки, средний возраст, стоимость, город."""
    context = record.get("to_club_context") or {}
    if not context:
        return ""
    parts = []
    lead = "Клуб %s" % to_club
    if league:
        lead += " выступает в %s" % league
    city = context.get("city")
    if city:
        lead += ("," if league else "") + " базируется в городе %s" % city
    parts.append(lead + ".")

    value = tm_money(context.get("squad_value"))
    avg = tm_money(context.get("average_player_value"))
    age = context.get("average_age")
    numbers = []
    if value:
        numbers.append("суммарная стоимость состава — %s" % value)
    if avg:
        numbers.append("средний игрок стоит %s" % avg)
    if age:
        numbers.append("средний возраст — %s года" % str(age).replace(".", ","))
    if numbers:
        parts.append("По оценке Transfermarkt " + ", ".join(numbers) + ".")
    return " ".join(parts)


def build_rumor_body(record: dict, status: str, fee_ru: str,
                     position_ru: str, country_ru: str,
                     from_api=None, to_api=None, league: str = "") -> str:
    """Текст страницы слуха.

    Раньше выходило 40-100 слов. Столько не ранжируется ни по какому запросу,
    а при потоке в сутки такие страницы тянут вниз весь домен: качество Google
    оценивает по сайту целиком, и тонкие страницы утягивают за собой те, что
    сделаны нормально.

    Собираем 350-450 слов целиком из того, что уже лежит в записи: оценки
    Transfermarkt, прежние клубы, амплуа, рост, место рождения, срок
    контракта, дебют за сборную. Ничего не выдумываем: нет данных — нет
    раздела.
    """
    player = record.get("player_full_name") or record["player"]
    to_club = record["to_club"]
    from_club = record.get("from_club") or ""
    points = record.get("market_value_points") or []
    source = record.get("source") or {}
    date_ru = ru_date(source.get("published_iso") or "")
    to_linked = club_link(to_api, to_club)
    from_linked = club_link(from_api, from_club)

    stage = {
        "agreement": "стороны согласовали условия перехода",
        "negotiations": "стороны ведут переговоры о переходе",
        "rumour": "обсуждается возможный переход",
    }.get(status, "обсуждается возможный переход")

    lines = ["## %s и %s: что известно" % (player, club_word(to_club, "nom")), ""]

    opening = "По информации %s, %s **%s**" % (
        source.get("publisher") or "СМИ", stage, player)
    if from_club:
        opening += " из %s" % club_word("**%s**" % from_club, "gen")
    opening += " в %s." % club_word("**%s**" % to_club, "acc")
    if date_ru:
        opening += " Сообщение появилось %s." % date_ru
    lines += [opening, ""]

    stage_note = {
        "agreement": ("Согласование условий — предпоследняя ступень: остаются "
                      "медицинское обследование и объявление клуба."),
        "negotiations": ("Переговоры означают, что клубы общаются напрямую, но "
                         "сумма и условия ещё не сведены."),
        "rumour": ("Интерес — самая ранняя ступень. До предложения дело может и "
                   "не дойти: клубы обычно прорабатывают несколько вариантов "
                   "сразу и выбирают один."),
    }.get(status, "")
    if stage_note:
        lines += [stage_note, ""]

    if fee_ru:
        lines += ["Обсуждаемая сумма — %s. Подтверждения у неё нет: цифру "
                  "называют СМИ, а не клубы." % fee_ru, ""]

    story = value_story(points)
    if story:
        lines += ["## Сколько стоит игрок", "", story, ""]

    lines += ["## Об игроке", ""]
    facts = []
    if position_ru:
        facts.append("**Позиция:** %s" % position_ru.lower())
    if record.get("age"):
        facts.append("**Возраст:** %s" % record["age"])
    if record.get("birth_date"):
        facts.append("**Дата рождения:** %s" % dotted_date(record["birth_date"]))
    if (record.get("birth_place") or "").strip():
        facts.append("**Место рождения:** %s" % record["birth_place"].strip())
    if country_ru:
        facts.append("**Гражданство:** %s" % country_ru)
    if record.get("height"):
        # В записи рост числом вида 1.85 — по-русски это «1,85 м».
        facts.append("**Рост:** %s м" % str(record["height"]).replace(".", ","))
    if from_club:
        facts.append("**Текущий клуб:** %s" % from_linked)
    if record.get("contract_until"):
        facts.append("**Контракт до:** %s" % dotted_date(record["contract_until"]))
    facts.append("**Клуб интереса:** %s" % to_linked)
    facts.append("**Статус темы:** %s"
                 % STATUS_LABELS.get(status, ("", "не подтверждено", ""))[1])
    lines += ["- %s" % fact for fact in facts]
    lines.append("")

    former = parse_former_clubs(record.get("former_clubs_note") or "")
    if former:
        lines += ["## Карьера", "",
                  "Ранее выступал за: %s." % ", ".join(
                      "%s (%s)" % (club, years) for club, years in former), ""]

    debut = record.get("national_team_debut")
    if debut and country_ru:
        lines += ["За сборную %s дебютировал %s."
                  % (country_genitive(country_ru), ru_date(debut)), ""]

    competition = competition_story(record, position_ru, to_club)
    portrait = club_portrait(record, to_club, league)
    if competition or portrait:
        lines += ["## Куда он может попасть", ""]
        if portrait:
            lines += [portrait, ""]
        if competition:
            lines += [competition, ""]

    if record.get("contract_until"):
        lines += ["Контракт с нынешним клубом рассчитан до %s. Чем ближе его "
                  "конец, тем дешевле обходится переход: за год до истечения "
                  "клубы обычно уже готовы торговаться, а за полгода игрок "
                  "вправе договариваться с кем угодно сам."
                  % dotted_date(record["contract_until"]), ""]

    lines += ["## Что это значит для клубов", ""]
    note = "Клуб %s ищет усиление" % to_club
    if position_ru:
        note += " на позицию «%s»" % position_ru.lower()
    note += "."
    note += " Состав и стоимость команды — на странице %s." % to_linked
    if from_club:
        note += (" Текущая команда игрока — %s: там же видно, кого клуб терял "
                 "и приобретал в этом окне." % from_linked)
    lines += [note, ""]

    lines += ["## Что будет дальше", "",
              "Официального объявления пока нет, поэтому материал остаётся в "
              "разделе «Слухи». Состоявшимся переход мы считаем только тогда, "
              "когда игрок появляется в составе клуба на Transfermarkt — до "
              "этого никакие сообщения СМИ статуса не меняют. Как только это "
              "случится, материал переедет в раздел «Трансферы» с полными "
              "данными и графиком стоимости, а нынешний адрес будет вести "
              "туда же.", ""]

    if source.get("publisher"):
        lines += ["---", "",
                  "**Источник:** %s. Данные игрока — Transfermarkt."
                  % source["publisher"]]
    return "\n".join(lines)


def publish_rumor(record: dict, tm_clubs: dict, bridge: dict,
                  countries: dict, allow_network: bool = False) -> dict:
    # Лестница статусов: интерес -> переговоры -> согласовано.
    # Разведка теперь различает "переговоры" по глаголу в заголовке
    # ("предложен клубу", "сделал предложение"), и терять эту ступень нельзя.
    status = {"agreement": "agreement",
              "negotiations": "negotiations"}.get(record.get("kind"), "rumour")
    label, display, css = STATUS_LABELS[status]

    player = record.get("player_full_name") or record["player"]
    to_club = record["to_club"]
    from_club = record.get("from_club") or ""
    if not from_club:
        return {"ok": False, "error": "не определён прежний клуб"}

    to_api, _ = resolve_api_id(to_club, tm_clubs, bridge, allow_network)
    from_api, _ = resolve_api_id(from_club, tm_clubs, bridge, allow_network)
    if not to_api or not from_api:
        return {"ok": False, "error": "не определены API-Football id клубов"}

    to_info, from_info = club_entry(to_api), club_entry(from_api)
    country = countries.get(
        str((record.get("nationality_ids") or {}).get("nationalityId") or ""))
    country_ru = country["name_ru"] if country else ""
    position_ru = POSITIONS.get(record.get("position") or "", ("", ""))[0]
    fee_ru = money_ru(record.get("fee_raw") or "")

    # Усыновлённая страница сохраняет свой адрес: он может быть в индексе,
    # а два адреса с одним содержимым — дубль, который вредит обоим.
    slug = record.get("rumor_slug_override") or rumor_slug(record)
    url = "/rumors/%s/" % slug
    league_id, league = LEAGUE_BY_COUNTRY.get(to_info.get("country") or "", ("", ""))

    title = "%s и %s: %s" % (player, to_club, display)
    description = ("Что известно о возможном переходе %s из %s в %s."
                   % (player, club_word(from_club, "gen"),
                      club_word(to_club, "acc")))

    front = [
        "---",
        'title: "%s"' % title,
        'description: "%s"' % description,
        'date: "%s"' % datetime.now().astimezone().isoformat(timespec="seconds"),
        'url: "%s"' % url,
        "draft: false",
        'type: "rumors"',
        'layout: "single"',
        'display_date: "%s"' % datetime.now().strftime("%d.%m.%Y"),
        'player: "%s"' % player,
        'from_club: "%s"' % from_club,
        'from_logo: "%s"' % (from_info.get("logo") or ""),
        'to_club: "%s"' % to_club,
        'to_logo: "%s"' % (to_info.get("logo") or ""),
        'fee: "%s"' % (fee_ru or "Сумма не называется"),
        'status: "%s"' % status,
        'status_label: "%s"' % label,
        'league_id: "%s"' % league_id,
        'league: "%s"' % league,
        'transfermarkt_player_id: %s' % (record.get("tm_player_id") or 0),
        'autopilot_entity_id: "%s"' % record.get("entity_id", ""),
        "---",
        "",
    ]
    body = build_rumor_body(record, status, fee_ru, position_ru, country_ru,
                            from_api, to_api, league)

    # Порог объёма. Страница в полсотни слов не ранжируется ни по какому
    # запросу, а поток таких страниц тянет вниз весь домен: качество Google
    # оценивает по сайту целиком. Нечем наполнить — лучше не публиковать
    # вовсе, запись останется в очереди и дождётся недостающих данных.
    words = len(re.findall(r"\w+", body))
    if words < MIN_RUMOR_WORDS:
        return {"ok": False,
                "error": "слишком короткая статья: %d слов при пороге %d"
                         % (words, MIN_RUMOR_WORDS)}

    page_dir = RUMORS_DIR / slug
    page_dir.mkdir(parents=True, exist_ok=True)
    (page_dir / "index.md").write_text("\n".join(front) + body + "\n",
                                       encoding="utf-8")

    # Запись в блок слухов на главной.
    homepage = json.loads(HOMEPAGE_JSON.read_text(encoding="utf-8"))
    rumors = [row for row in (homepage.get("rumors") or [])
              if row.get("slug") != slug]
    rumors.insert(0, {
        "slug": slug,
        "url": url.lstrip("/"),
        "title": title,
        "player": player,
        "status": status,
        "status_display": display,
        "status_css": css,
        "group": "rumor",
        "date": datetime.now().astimezone().isoformat(timespec="seconds"),
        "sort_ts": datetime.now().timestamp(),
        "from_name": from_club,
        "to_name": to_club,
        "from_logo": from_info.get("logo") or "",
        "to_logo": to_info.get("logo") or "",
        "fee": fee_ru or "Сумма не называется",
        "from_club_id": str(from_api),
        "to_club_id": str(to_api),
    })
    homepage["rumors"] = rumors
    HOMEPAGE_JSON.write_text(
        json.dumps(homepage, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    return {"ok": True, "slug": slug, "url": url,
            "words": len(re.findall(r"\w+", body))}


def remove_rumor(slug: str) -> list[str]:
    """Убирает слух с сайта. Вызывается при повышении до трансфера."""
    removed = []
    page_dir = RUMORS_DIR / slug
    if page_dir.exists():
        shutil.rmtree(page_dir)
        removed.append("страница слуха удалена")
    homepage = json.loads(HOMEPAGE_JSON.read_text(encoding="utf-8"))
    rumors = homepage.get("rumors") or []
    left = [row for row in rumors if row.get("slug") != slug]
    if len(left) != len(rumors):
        homepage["rumors"] = left
        HOMEPAGE_JSON.write_text(
            json.dumps(homepage, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8")
        removed.append("запись в блоке слухов удалена")
    return removed


def _front_matter(path: Path) -> dict:
    """Поля из шапки страницы. Значения простые, разбирать YAML целиком незачем."""
    text = path.read_text(encoding="utf-8", errors="replace")
    if not text.startswith("---"):
        return {}
    head = text.split("---", 2)[1]
    out = {}
    for line in head.splitlines():
        m = re.match(r'^\s*([a-z_]+)\s*:\s*"?(.*?)"?\s*$', line)
        if m:
            out[m.group(1)] = m.group(2)
    return out


def resync_homepage() -> int:
    """Пересобирает блок слухов на главной из страниц раздела.

    Запись на главную делается при публикации, и слухи, заведённые до того,
    как этот шаг появился, туда не попали: на сайте страница есть, в блоке её
    нет. Отсюда и пустые слоты — панель слухов вдвое короче панели трансферов,
    хотя материала хватает.

    Источник правды здесь — сами страницы: что лежит в content/rumors, то и
    показываем. Записи, ведущие в раздел трансферов (старые слухи жили там),
    сохраняются как есть — страницы для них никуда не делись.
    """
    # Старые страницы ссылаются на сырые выгрузки API-Football
    # (images/clubs/api/530.png), новые — на обработанные, обрезанные по
    # краям. В строке это заметно: у «Атлетико» сырой файл весит 70 КБ и
    # почти весь состоит из прозрачных полей, поэтому знак выходит мелким
    # рядом с соседями. Подменяем на обработанный, когда он есть в каталоге.
    catalog = {}
    try:
        raw = json.loads(CLUB_LOGOS.read_text(encoding="utf-8"))
        catalog = raw.get("clubs", raw) or {}
    except Exception:
        pass

    def best_logo(path: str) -> str:
        match = re.search(r"/(\d+)\.png$", path or "")
        if not match:
            return path
        better = (catalog.get(match.group(1)) or {}).get("logo") or ""
        return better or path

    homepage = json.loads(HOMEPAGE_JSON.read_text(encoding="utf-8"))
    existing = {row.get("slug"): row for row in (homepage.get("rumors") or [])}
    kept_foreign = [row for row in (homepage.get("rumors") or [])
                    if not str(row.get("url", "")).startswith("rumors/")]

    rows = []
    for page in sorted(RUMORS_DIR.glob("*/index.md")):
        slug = page.parent.name
        fm = _front_matter(page)
        if not fm.get("player"):
            continue
        status = fm.get("status") or "rumour"
        label, display, css = STATUS_LABELS.get(status, STATUS_LABELS["rumour"])
        date = fm.get("date") or ""
        try:
            ts = datetime.fromisoformat(date).timestamp()
        except Exception:
            ts = 0.0
        previous = existing.get(slug, {})
        rows.append({
            "slug": slug,
            "url": (fm.get("url") or "/rumors/%s/" % slug).lstrip("/"),
            "title": fm.get("title") or "",
            "player": fm.get("player"),
            "status": status,
            "status_display": display,
            "status_css": css,
            "group": "rumor",
            "date": date,
            "sort_ts": ts,
            "from_name": fm.get("from_club") or "",
            "to_name": fm.get("to_club") or "",
            "from_logo": best_logo(fm.get("from_logo") or previous.get("from_logo") or ""),
            "to_logo": best_logo(fm.get("to_logo") or previous.get("to_logo") or ""),
            "fee": fm.get("fee") or "Сумма не называется",
            "from_club_id": previous.get("from_club_id", ""),
            "to_club_id": previous.get("to_club_id", ""),
        })

    known = {row["slug"] for row in rows}
    rows.extend(row for row in kept_foreign if row.get("slug") not in known)
    rows.sort(key=lambda r: -(r.get("sort_ts") or 0))

    # Один игрок — одна строка. Часть слухов живёт двумя страницами: старая
    # в разделе трансферов и новая в разделе слухов, и без отсева Бернарду
    # Силва с Альваресом появлялись в блоке дважды. Сравниваем имена без
    # диакритики: в одной записи «Julián Álvarez», в другой «Julian Alvarez».
    def key(row: dict) -> str:
        name = unicodedata.normalize("NFKD", row.get("player") or "")
        return "".join(c for c in name if not unicodedata.combining(c)).casefold().strip()

    seen: dict[str, dict] = {}
    for row in rows:
        k = key(row)
        if not k:
            continue
        # Запись новее — она и остаётся; при равных датах предпочитаем
        # страницу из раздела слухов, он теперь канонический.
        old = seen.get(k)
        if old is None:
            seen[k] = row
            continue
        newer = (row.get("sort_ts") or 0) > (old.get("sort_ts") or 0)
        same_time = (row.get("sort_ts") or 0) == (old.get("sort_ts") or 0)
        canonical = str(row.get("url", "")).startswith("rumors/")
        if newer or (same_time and canonical):
            seen[k] = row
    dropped = len(rows) - len(seen)
    rows = sorted(seen.values(), key=lambda r: -(r.get("sort_ts") or 0))
    if dropped:
        print("  снято дублей по игроку: %d" % dropped)

    was = len(homepage.get("rumors") or [])
    homepage["rumors"] = rows
    HOMEPAGE_JSON.write_text(
        json.dumps(homepage, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("  блок слухов на главной: было %d, стало %d" % (was, len(rows)))
    for row in rows:
        print("    %-20s %-24s -> %-22s %s"
              % (row["player"][:20], row["from_name"][:24],
                 row["to_name"][:22], row["status_display"]))
    return len(rows)


def adopt_pages() -> int:
    """Заводит записи для страниц слухов, у которых их нет.

    Пять июльских страниц сделаны до появления парсера: в разделе они есть,
    а в очереди их нет, поэтому перевыпустить с нормальным текстом нечем — у
    них так и остаётся по сорок слов. Собираем запись из шапки страницы и
    ставим в состояние DISCOVERED: дальше обычное обогащение само найдёт
    игрока, стоимость и состав, а публикация перезапишет страницу.

    Адрес сохраняется прежним. Он у старых страниц со статусом в хвосте
    (...-agreement, ...-interest), и менять его нельзя: страница может быть
    в индексе, а два адреса с одним содержимым — это дубль, который вредит
    обоим.
    """
    known = set()
    for path in RECORDS_DIR.glob("*.json"):
        try:
            slug = json.loads(path.read_text(encoding="utf-8")).get("rumor_slug")
        except Exception:
            continue
        if slug:
            known.add(slug)

    made = 0
    for page in sorted(RUMORS_DIR.glob("*/index.md")):
        slug = page.parent.name
        if slug in known:
            continue
        fm = _front_matter(page)
        player = fm.get("player")
        to_club = fm.get("to_club")
        from_club = fm.get("from_club")
        if not (player and to_club and from_club):
            print("  пропуск %s: в шапке нет игрока или клубов" % slug)
            continue

        status = fm.get("status") or "rumour"
        kind = {"negotiations": "negotiations",
                "agreement": "agreement"}.get(status, "rumour")
        entity = "%s__%s__%s" % (slugify(player.split()[-1]),
                                 slugify(from_club), slugify(to_club))
        target = RECORDS_DIR / ("%s.json" % entity)
        if target.exists():
            continue

        target.write_text(json.dumps({
            "schema_version": 2,
            "kind": kind,
            "entity_id": entity,
            "player": player.split()[-1],
            "player_full_name": player,
            "from_club": from_club,
            "to_club": to_club,
            "fee_raw": fm.get("fee") or "",
            "verdict": "NEW_CANDIDATE",
            "pipeline_state": "DISCOVERED",
            "adopted_from_page": slug,
            "rumor_slug_override": slug,
            "source": {
                "publisher": "СМИ",
                "tier": "major_media",
                "url": "",
                "title": fm.get("title") or "",
                "published_iso": fm.get("date") or "",
            },
            "discovered_at": now_iso(),
        }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        made += 1
        print("  усыновлена %-44s %s -> %s" % (slug[:44], from_club, to_club))
    print("  заведено записей: %d" % made)
    return made


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Publish rumours from the queue")
    parser.add_argument("--save", action="store_true", help="реально публиковать")
    parser.add_argument("--network", action="store_true")
    parser.add_argument("--resync-homepage", action="store_true",
                        help="пересобрать блок слухов на главной из страниц раздела")
    parser.add_argument("--limit", type=int, default=0,
                        help="сколько слухов выпустить за раз (0 — все готовые)")
    parser.add_argument("--adopt-pages", action="store_true",
                        help="завести записи для страниц слухов без записи")
    args = parser.parse_args(argv)

    if args.adopt_pages:
        print("\n=== УСЫНОВЛЕНИЕ СТАРЫХ СТРАНИЦ ===")
        adopt_pages()
        return 0

    if args.resync_homepage:
        print("\n=== ПЕРЕСБОРКА БЛОКА СЛУХОВ ===")
        resync_homepage()
        return 0

    tm_clubs = build_tm_club_index(verbose=False)
    bridge = load_club_bridge()
    countries = load_country_map()

    print("\n=== ПУБЛИКАЦИЯ СЛУХОВ ===")
    published = 0
    for path in sorted(RECORDS_DIR.glob("*.json")):
        try:
            record = json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            continue
        if record.get("pipeline_state") != "RUMOR_READY":
            continue

        if not args.save:
            print("  [DRY] %s : %s -> %s" % (
                record.get("player_full_name"), record.get("from_club"),
                record.get("to_club")))
            continue

        if args.limit and published >= args.limit:
            print("  норма такта исчерпана, остальные ждут следующего")
            break

        result = publish_rumor(record, tm_clubs, bridge, countries, args.network)
        if result.get("ok"):
            record["pipeline_state"] = "PUBLISHED_AS_RUMOR"
            record["rumor_slug"] = result["slug"]
            record["rumor_published_at"] = now_iso()
            path.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n",
                            encoding="utf-8")
            published += 1
            print("  ОПУБЛИКОВАН СЛУХ  %s  (%d слов)"
                  % (result["url"], result["words"]))
        else:
            print("  НЕ ПОЛУЧИЛОСЬ  %s : %s"
                  % (record.get("player"), result.get("error")))

    print("\n  опубликовано слухов: %d\n" % published)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
