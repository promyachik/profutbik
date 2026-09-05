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


def build_rumor_body(record: dict, status: str, fee_ru: str,
                     position_ru: str, country_ru: str) -> str:
    player = record.get("player_full_name") or record["player"]
    to_club = record["to_club"]
    from_club = record.get("from_club") or ""
    points = record.get("market_value_points") or []
    market = euro(points[-1]["value_eur_m"]) if points else ""
    date_ru = ru_date((record.get("source") or {}).get("published_iso") or "")

    stage = {
        "agreement": "стороны согласовали условия",
        "negotiations": "стороны ведут переговоры",
        "rumour": "тема обсуждается",
    }.get(status, "тема обсуждается")

    lines = ["## %s и %s: что известно" % (player, club_word(to_club, "nom"))]
    lines.append("")

    opening = "По информации %s, %s о переходе **%s**" % (
        (record.get("source") or {}).get("publisher") or "СМИ", stage, player)
    if from_club:
        opening += " из %s" % club_word("**%s**" % from_club, "gen")
    opening += " в %s." % club_word("**%s**" % to_club, "acc")
    if date_ru:
        opening += " Сообщение появилось %s." % date_ru
    lines += [opening, ""]

    lines.append(
        "Официального объявления пока нет, поэтому материал остаётся в разделе "
        "«Слухи». Как только переход будет подтверждён, он появится в разделе "
        "«Трансферы» с полными данными.")
    lines.append("")

    lines += ["## Об игроке", ""]
    facts = []
    if position_ru:
        facts.append("**Позиция:** %s" % position_ru.lower())
    if from_club:
        facts.append("**Текущий клуб:** %s" % from_club)
    facts.append("**Клуб интереса:** %s" % to_club)
    if country_ru:
        facts.append("**Гражданство:** %s" % country_ru)
    if record.get("birth_date"):
        facts.append("**Дата рождения:** %s" % dotted_date(record["birth_date"]))
    if market:
        facts.append("**Рыночная стоимость Transfermarkt:** %s" % market)
    if fee_ru:
        facts.append("**Обсуждаемая сумма:** %s" % fee_ru)
    facts.append("**Статус:** %s" % STATUS_LABELS.get(
        status, ("", "не подтверждено", ""))[1])
    lines += ["- %s" % fact for fact in facts]

    former = parse_former_clubs(record.get("former_clubs_note") or "")
    if former:
        lines += ["", "## Карьера", "",
                  "Ранее выступал за: %s." % ", ".join(
                      "%s (%s)" % (club, years) for club, years in former)]

    debut = record.get("national_team_debut")
    if debut and country_ru:
        lines += ["", "За сборную %s дебютировал %s."
                  % (country_genitive(country_ru), ru_date(debut))]

    source = record.get("source") or {}
    if source.get("publisher"):
        lines += ["", "---", "", "**Источник:** %s. Данные игрока — Transfermarkt."
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

    slug = rumor_slug(record)
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
    body = build_rumor_body(record, status, fee_ru, position_ru, country_ru)

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
            "from_logo": fm.get("from_logo") or previous.get("from_logo") or "",
            "to_logo": fm.get("to_logo") or previous.get("to_logo") or "",
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


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Publish rumours from the queue")
    parser.add_argument("--save", action="store_true", help="реально публиковать")
    parser.add_argument("--network", action="store_true")
    parser.add_argument("--resync-homepage", action="store_true",
                        help="пересобрать блок слухов на главной из страниц раздела")
    parser.add_argument("--limit", type=int, default=0,
                        help="сколько слухов выпустить за раз (0 — все готовые)")
    args = parser.parse_args(argv)

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
