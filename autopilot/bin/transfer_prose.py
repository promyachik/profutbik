"""
PROMYACHIK - НЕДОСТАЮЩИЕ РАЗДЕЛЫ СТРАНИЦЫ ТРАНСФЕРА

Замер по 107 страницам: медиана 209 слов в теле, у самой короткой 67. При
этом движок 3.4 умеет писать куда больше - разбор состава, место рождения,
карточку игрока, - но пишет только когда обогащение принесло все поля. Когда
не принесло, раздел просто не выводится, и страница выходит куцей.

    "Что получает клуб"      было на 14 страницах из 107
    "Карточка игрока"        на 14
    конкуренция на позиции   на 36
    место в рейтинге состава на 37

Здесь эти разделы дописываются задним числом - но не из сети, а из того, что
уже лежит у нас на диске:

    страницы клубов          состав нового клуба целиком: возраст, позиция и
                             оценка каждого игрока. Отсюда и роль новичка -
                             какое место по стоимости, кто конкурент, скольких
                             партнёров он моложе
    график стоимости         путь игрока по клубам с оценкой на каждом шаге

ЧЕГО ЗДЕСЬ НЕТ

Раздела, который на странице уже есть: дописывать второй "Что получает клуб"
хуже, чем не дописывать ничего. Проверка идёт по заголовку и по характерной
фразе, а не по длине.

Придуманных фактов тоже нет. Нет клубной страницы у клуба назначения - нет и
абзаца про состав. Не нашли игрока в составе - нет абзаца про роль. Молчание
дешевле выдумки.

Латинские названия клубов не склоняются: подлежащее - слово "клуб".
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

BIN = Path(__file__).resolve().parent
sys.path.insert(0, str(BIN))
from transfer_discovery import ACTIVE_PROJECT, normalize  # noqa: E402
from job_builder import club_word, plural_ru  # noqa: E402
import club_prose  # noqa: E402

CLUBS_DIR = ACTIVE_PROJECT / "content" / "clubs"
CHART_JS = ACTIVE_PROJECT / "static" / "js" / "transfer-player-market-value-chart.js"

_clubs: dict[str, dict] | None = None
_chart: dict[str, dict] | None = None


def same_club(left: str, right: str) -> bool:
    """Один ли это клуб. «Arsenal» и «Arsenal FC» - да, «Real Madrid» и
    «Real Madrid Castilla» - нет: сравнение идёт по границам слов."""
    a, b = normalize(left or ""), normalize(right or "")
    if not a or not b:
        return False
    if a == b:
        return True
    aw, bw = a.split(), b.split()
    return aw[: len(bw)] == bw or bw[: len(aw)] == aw


def clubs() -> dict[str, dict]:
    """Клубы с составом - из наших же страниц, без единого запроса."""
    global _clubs
    if _clubs is not None:
        return _clubs
    out: dict[str, dict] = {}
    for page in sorted(CLUBS_DIR.glob("*/index.md")):
        text = page.read_text(encoding="utf-8", errors="replace")
        if not text.startswith("---"):
            continue
        head = text.split("---", 2)[1]
        name = re.search(r'(?m)^club_name:\s*"([^"]*)"', head)
        if not name:
            continue
        squad = []
        for block in re.finditer(
                r'(?ms)^  - name: "([^"]*)"\n'
                r'    position: "([^"]*)"\n'
                r'    position_short: "([^"]*)"\n'
                r"    age: (\S+)\n"
                r'    value: "([^"]*)"', head):
            age = block.group(4)
            squad.append({
                "name": block.group(1), "position": block.group(2),
                "position_short": block.group(3),
                "age": int(age) if age.isdigit() else None,
                "value_display": block.group(5),
            })
        def scalar(key: str) -> str:
            found = re.search(r'(?m)^%s:\s*"?(.*?)"?\s*$' % re.escape(key), head)
            return found.group(1) if found else ""

        size = scalar("squad_size")
        out[name.group(1)] = {
            "slug": page.parent.name,
            "name": name.group(1),
            "city": scalar("club_city"),
            "league": scalar("league"),
            "squad_size": int(size) if size.isdigit() else len(squad),
            "average_age": scalar("average_age"),
            "squad_value": scalar("squad_value"),
            "average_value": scalar("average_value"),
            "squad": squad,
        }
    _clubs = out
    return out


def club_by_name(name: str) -> dict | None:
    table = clubs()
    if name in table:
        return table[name]
    for key, value in table.items():
        if same_club(key, name):
            return value
    return None


def chart() -> dict[str, dict]:
    """Путь игрока по клубам из данных графика. Ключ - slug страницы."""
    global _chart
    if _chart is not None:
        return _chart
    _chart = {}
    if not CHART_JS.exists():
        return _chart
    text = CHART_JS.read_text(encoding="utf-8", errors="replace")
    start = text.find("[{")
    if start < 0:
        return _chart
    depth, end = 0, -1
    for index in range(start, len(text)):
        if text[index] == "[":
            depth += 1
        elif text[index] == "]":
            depth -= 1
            if depth == 0:
                end = index + 1
                break
    if end < 0:
        return _chart
    try:
        rows = json.loads(text[start:end])
    except Exception:
        return _chart
    for row in rows:
        for path in row.get("paths") or []:
            _chart[str(path).strip("/").split("/")[-1]] = row
    return _chart


def role_paragraph(player: str, club: dict, position: str, age) -> str:
    """Место новичка в составе: стоимость, конкуренты, возраст."""
    squad = club.get("squad") or []
    if len(squad) < 10:
        return ""
    place = next((i for i, p in enumerate(squad, 1)
                  if normalize(p["name"]) == normalize(player)), 0)
    if not place:
        return ""
    parts = ["В рейтинге стоимости состава он занимает %d-е место из %d."
             % (place, len(squad))]

    mine = squad[place - 1]
    rivals = [p["name"] for p in squad
              if p is not mine and p.get("position_short")
              and p["position_short"] == mine.get("position_short")]
    if rivals:
        # Согласование по числу. «Составят ещё 1 игрок» - типовая машинная
        # ошибка, которую читатель замечает сразу.
        if len(rivals) == 1:
            head_line = "Конкуренцию на этой позиции составит ещё один игрок: %s." % rivals[0]
        else:
            head_line = ("Конкуренцию на этой позиции составят ещё %d %s: %s."
                         % (len(rivals),
                            plural_ru(len(rivals), "игрок", "игрока", "игроков"),
                            ", ".join(rivals[:5])))
        parts.insert(0, head_line)
    own_age = mine.get("age") or (int(age) if str(age).isdigit() else None)
    if own_age:
        younger = len([p for p in squad if p.get("age") and p["age"] > own_age])
        if younger:
            parts.append("В свои %d %s он моложе %d %s команды."
                         % (own_age, plural_ru(own_age, "год", "года", "лет"),
                            younger,
                            plural_ru(younger, "партнёра", "партнёров", "партнёров")))
    return " ".join(parts)


def club_paragraph(club: dict) -> str:
    """Куда игрок пришёл. Со ссылкой на нашу же страницу клуба - до сих пор
    страница трансфера не вела никуда, кроме источника."""
    bits = []
    if club.get("squad_size"):
        bits.append("В составе %s теперь %d %s"
                    % (club_word(club["name"], "gen"), club["squad_size"],
                       plural_ru(club["squad_size"], "игрок", "игрока", "игроков")))
        if club.get("average_age"):
            bits[-1] += " со средним возрастом %s года" % club["average_age"]
        bits[-1] += "."
    if club.get("squad_value"):
        line = "Общая стоимость команды по Transfermarkt — %s" % club["squad_value"]
        if club.get("average_value"):
            line += ", в среднем %s на игрока" % club["average_value"]
        bits.append(line + ".")
    if club.get("city"):
        bits.append("Домашние матчи команда проводит в городе %s." % club["city"])
    if not bits:
        return ""
    bits.append("Подробный состав — на странице клуба [%s](/clubs/%s/)."
                % (club["name"], club["slug"]))
    return " ".join(bits)


def career_paragraph(row: dict, player: str) -> str:
    """Путь по клубам с оценкой на каждом шаге - из данных графика."""
    points = row.get("points") or []
    steps, seen = [], None
    for point in points:
        club = (point.get("club") or {}).get("name") or ""
        if not club or club == seen:
            continue
        seen = club
        steps.append((club, point.get("label") or "", point.get("value_label") or ""))
    # Двух клубов уже достаточно: «Монако -> Ньюкасл» с оценкой на каждом шаге
    # - это факт, которого в тексте страницы нет. График рисуется картинкой,
    # то есть поисковику эти цифры недоступны вовсе.
    if len(steps) < 2 or len(points) < 3:
        return ""
    told = ", ".join("%s (%s, %s)" % (club, label, value)
                     for club, label, value in steps[:6])
    values = [p.get("value") for p in points if isinstance(p.get("value"), (int, float))]
    text = "Как менялась оценка игрока по клубам: %s." % told
    if len(values) >= 3:
        peak = max(values)
        now = values[-1]
        if peak > now:
            text += (" Пик пришёлся на %s: с тех пор оценка снизилась на %d%%."
                     % (next(p.get("label") for p in points if p.get("value") == peak),
                        round((peak - now) * 100 / peak)))
        elif now > min(values):
            text += " Сейчас игрок стоит дороже, чем в начале пути."
    return text
