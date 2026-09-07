"""
PROMYACHIK - ТЕКСТ КЛУБНОЙ СТРАНИЦЫ

Зачем. В Search Console у сайта ноль проиндексированных страниц. Технических
запретов нет: robots пускает, noindex нигде, sitemap обработан успешно. Google
обошёл пятнадцать адресов из 249 и остановился с формулировкой "просканирована,
но пока не проиндексирована" - то есть посмотрел и решил, что брать нечего.

Замер объясняет почему. Клубных страниц 148 - больше половины сайта, - и на
каждой было 43 слова собственного текста. Для сравнения: у слухов 352, и
только потому, что там в коде стоит порог MIN_RUMOR_WORDS. У клубов порога не
было вовсе.

ЧТО ЗДЕСЬ ПОЯВИЛОСЬ

Ни одного придуманного факта. Всё считается из состава, который и так лежит в
шапке страницы: возраст, позиция, оценка Transfermarkt у каждого игрока.

    возрастной профиль     кто самый молодой и самый возрастной, сколько
                           до 21 года и сколько за тридцать
    линии                  сколько вратарей, защитников, полузащитников и
                           нападающих, и на какую линию приходятся деньги
    концентрация           сколько стоит пятёрка самых дорогих и какую долю
                           состава она составляет
    место в лиге           каким по стоимости состава клуб идёт в своём
                           турнире; считается по нашим же 148 страницам
    переходы               список со ссылками на наши страницы трансферов

Последнее важно отдельно: до сих пор клубная страница не ссылалась никуда, и
обходу было некуда идти. Теперь каждая ведёт в раздел трансферов.

ЧЕГО ЗДЕСЬ НЕТ

Оборотов ради объёма. Если данных на абзац не хватает - у клуба нет переходов,
не проставлены возрасты, - абзац просто не выводится. Пустая страница честнее
раздутой: за воду Google наказывает ровно так же, как за пустоту.

Латинские названия клубов не склоняются и рода в русском не имеют. Подлежащее
везде - слово "клуб", склоняется оно (club_word).
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

BIN = Path(__file__).resolve().parent
sys.path.insert(0, str(BIN))
from transfer_discovery import ACTIVE_PROJECT  # noqa: E402
from job_builder import club_word, plural_ru  # noqa: E402

CLUBS_DIR = ACTIVE_PROJECT / "content" / "clubs"

# Transfermarkt делит заявку на четыре линии; краевые полузащитники у него в
# полузащите, а вингеры - в атаке. Придерживаемся его деления, чтобы цифры на
# странице сходились с источником, откуда взяты позиции.
LINES = [
    ("вратарей", ("GK",)),
    ("защитников", ("CB", "LB", "RB")),
    ("полузащитников", ("DM", "CM", "AM", "LM", "RM")),
    ("нападающих", ("LW", "RW", "CF", "SS")),
]
LINE_NAMES = {
    "вратарей": "вратарская линия",
    "защитников": "оборона",
    "полузащитников": "полузащита",
    "нападающих": "атака",
}

_ranking: dict[str, list[tuple[str, int]]] | None = None


def money(value: float) -> str:
    """Евро словами: миллиарды и миллионы, как на Transfermarkt."""
    if value >= 1_000_000_000:
        return ("€%.2f млрд" % (value / 1_000_000_000)).replace(".", ",")
    if value >= 1_000_000:
        text = "€%.2f млн" % (value / 1_000_000)
        return text.replace(".00", "").replace(".", ",")
    if value >= 1000:
        return "€%d тыс." % round(value / 1000)
    return "€%d" % round(value)


def league_ranking() -> dict[str, list[tuple[str, int]]]:
    """Клубы каждой лиги по стоимости состава, от дорогих к дешёвым.

    Читается из наших же страниц, а не из сети: значения там свежие, их
    поставил тот же прогон, что строит страницы. Кэшируется на процесс -
    иначе на 148 клубов вышло бы 148 обходов папки.
    """
    global _ranking
    if _ranking is not None:
        return _ranking
    buckets: dict[str, list[tuple[str, int]]] = {}
    for page in sorted(CLUBS_DIR.glob("*/index.md")):
        text = page.read_text(encoding="utf-8", errors="replace")
        head = text.split("---", 2)[1] if text.startswith("---") else ""
        league = re.search(r'(?m)^league_id:\s*"([^"]*)"', head)
        value = re.search(r"(?m)^squad_value_eur:\s*(\d+)", head)
        name = re.search(r'(?m)^club_name:\s*"([^"]*)"', head)
        if not (league and value and name) or not int(value.group(1)):
            continue
        buckets.setdefault(league.group(1), []).append(
            (name.group(1), int(value.group(1))))
    for rows in buckets.values():
        rows.sort(key=lambda item: item[1], reverse=True)
    _ranking = buckets
    return _ranking


def _age_paragraph(squad: list[dict], name: str) -> str:
    aged = [p for p in squad if p.get("age")]
    if len(aged) < 5:
        return ""
    youngest = min(aged, key=lambda p: p["age"])
    oldest = max(aged, key=lambda p: p["age"])
    young = len([p for p in aged if p["age"] <= 21])
    old = len([p for p in aged if p["age"] >= 30])
    text = ("Самый молодой в заявке — %s, ему %d %s; самый возрастной — %s, %d."
            % (youngest["name"], youngest["age"],
               plural_ru(youngest["age"], "год", "года", "лет"),
               oldest["name"], oldest["age"]))
    parts = []
    if young:
        parts.append("до 21 года — %d %s"
                     % (young, plural_ru(young, "игрок", "игрока", "игроков")))
    if old:
        parts.append("тридцать и старше — %d" % old)
    if parts:
        text += " Молодых и опытных в составе так: %s." % ", ".join(parts)
    return text


def _lines_paragraph(squad: list[dict], total_value: int) -> str:
    counts, values = [], {}
    for label, codes in LINES:
        people = [p for p in squad if (p.get("position_short") or "") in codes]
        if people:
            counts.append("%s %d" % (label, len(people)))
            values[label] = sum(int(p.get("value") or 0) for p in people)
    if len(counts) < 3:
        return ""
    text = "По линиям заявка разложена так: %s." % ", ".join(counts)
    if total_value and values:
        top = max(values, key=values.get)
        share = round(values[top] * 100 / total_value)
        if share >= 25:
            text += (" Дороже всего клубу обходится %s — %s, это %d%% стоимости "
                     "состава." % (LINE_NAMES[top], money(values[top]), share))
    return text


def _concentration_paragraph(squad: list[dict], total_value: int) -> str:
    priced = sorted((p for p in squad if int(p.get("value") or 0)),
                    key=lambda p: int(p["value"]), reverse=True)
    if len(priced) < 8 or not total_value:
        return ""
    five = priced[:5]
    summed = sum(int(p["value"]) for p in five)
    share = round(summed * 100 / total_value)
    names = ", ".join(p["name"] for p in five)
    return ("Пятеро самых дорогих — %s — стоят вместе %s, то есть %d%% всей "
            "команды." % (names, money(summed), share))


def _league_paragraph(name: str, league_id: str, league_ru: str,
                      value: int) -> str:
    if not (league_id and value and league_ru):
        return ""
    rows = league_ranking().get(str(league_id)) or []
    if len(rows) < 6:
        return ""
    place = next((i for i, row in enumerate(rows, 1)
                  if row[0] == name), 0)
    if not place:
        return ""
    average = sum(row[1] for row in rows) // len(rows)
    text = ("По стоимости состава клуб идёт %d-м из %d в лиге «%s»."
            % (place, len(rows), league_ru))
    text += " Средний состав турнира оценён в %s." % money(average)
    if place == 1:
        text += " Дороже в лиге нет никого."
    elif place == len(rows):
        text += " Дешевле состава в лиге нет."
    return text


def _page_live(slug: str) -> bool:
    """Есть ли такая страница трансфера и не черновик ли она.

    Иначе клубная страница уводит в 404. Именно так и вышло с «Марио Гилой»:
    страница помечена draft, Hugo её не собирает, а ссылка с «Милана» на неё
    стояла. Проверять по собранному public нельзя - Hugo не подчищает старые
    файлы, и удалённая страница остаётся там лежать, создавая видимость.
    """
    page = ACTIVE_PROJECT / "content" / "transfers" / slug / "index.md"
    if not page.is_file():
        return False
    head = page.read_text(encoding="utf-8", errors="replace").split("---", 2)
    return len(head) > 1 and not re.search(r"(?m)^draft:\s*true\s*$", head[1])


def _transfers_paragraph(transfers: list[dict]) -> str:
    """Переходы со ссылками. Ради них абзац и написан: до сих пор клубная
    страница не вела никуда, и обходу некуда было идти."""
    rows = [t for t in transfers
            if t.get("slug") and t.get("player") and _page_live(t["slug"])]
    if not rows:
        return ""
    incoming = [t for t in rows if t.get("direction") == "in"]
    outgoing = [t for t in rows if t.get("direction") == "out"]

    def listing(items: list[dict], word: str) -> str:
        parts = []
        for item in items[:8]:
            link = "[%s](/transfers/%s/)" % (item["player"], item["slug"])
            other = item.get("other_club") or ""
            parts.append("%s (%s %s)" % (link, word, other) if other else link)
        return ", ".join(parts)

    chunks = []
    if incoming:
        chunks.append("пришли: %s" % listing(incoming, "из"))
    if outgoing:
        chunks.append("ушли: %s" % listing(outgoing, "в"))
    return "Переходы, о которых мы писали, — %s." % "; ".join(chunks)


def build(facts: dict) -> list[str]:
    """Абзацы текста клубной страницы.

    facts: name, league_id, league_ru, squad_size, average_age, squad_value,
    average_value, squad_value_eur, squad[], transfers[].
    """
    name = facts.get("name") or ""
    squad = facts.get("squad") or []
    total = int(facts.get("squad_value_eur") or 0)
    body: list[str] = []

    lead = "В заявке %s — %d %s" % (
        club_word(name, "gen"), facts.get("squad_size") or len(squad),
        plural_ru(facts.get("squad_size") or len(squad),
                  "игрок", "игрока", "игроков"))
    if facts.get("average_age"):
        lead += " со средним возрастом %s года" % facts["average_age"]
    lead += "."
    if facts.get("squad_value"):
        lead += (" Общая стоимость команды по оценке Transfermarkt — %s"
                 % facts["squad_value"])
        if facts.get("average_value"):
            lead += ", в среднем %s на игрока" % facts["average_value"]
        lead += "."
    body.append(lead)

    top = squad[0] if squad else None
    if top and top.get("value_display"):
        body.append("Самый дорогой игрок состава — %s (%s), его стоимость "
                    "оценивается в %s." % (top["name"],
                                           (top.get("position") or "").lower(),
                                           top["value_display"]))

    for paragraph in (
        _age_paragraph(squad, name),
        _lines_paragraph(squad, total),
        _concentration_paragraph(squad, total),
        _league_paragraph(name, facts.get("league_id") or "",
                          facts.get("league_ru") or "", total),
        _transfers_paragraph(facts.get("transfers") or []),
    ):
        if paragraph:
            body.append(paragraph)
    return body
