"""
PROMYACHIK - ПЕРЕПИСАТЬ ТЕКСТ 148 КЛУБНЫХ СТРАНИЦ

Тот же текст, что теперь строит club_prose, но применённый к страницам,
которые уже стоят на сайте. Без единого запроса в сеть: всё нужное лежит в
шапке самой страницы - состав с возрастом, позицией и оценкой каждого игрока,
стоимость команды, лига, переходы клуба.

Перестраивать через club_pages.py --all было бы честнее по свежести, но это
148 клубов по одному запросу состава плюс по запросу на каждого из 4179
игроков - около четырёх тысяч обращений к Transfermarkt ради текста, который
считается из уже имеющихся цифр.

ШАПКА НЕ ТРОГАЕТСЯ ВООБЩЕ

Меняется только то, что после закрывающего "---". Состав, стоимости, ссылки
на эмблемы остаются байт в байт: их ставит движок, и переписывать их отсюда
значит спорить с ним за одно и то же поле.

Стоимость игрока в шапке лежит строкой вида "€120 млн" - разбираем обратно в
число. Формат свой, его же и печатали, поэтому разбор точный. Строка, которую
разобрать не вышло, считается нулём и в суммы не попадает.

Запускается без ключей - показывает, что вышло бы. Меняет с --save.
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

BIN = Path(__file__).resolve().parent
sys.path.insert(0, str(BIN))
from transfer_discovery import ACTIVE_PROJECT, PARSER_ROOT  # noqa: E402
import club_prose  # noqa: E402

CLUBS_DIR = ACTIVE_PROJECT / "content" / "clubs"
BACKUPS = PARSER_ROOT.parent / "patch-backups"
REPORTS = PARSER_ROOT.parent / "reports"


def parse_money(text: str) -> int:
    """«€1,37 млрд» -> 1370000000. Формат наш собственный, из club_prose.money."""
    if not text:
        return 0
    match = re.search(r"([\d ]+(?:[.,]\d+)?)\s*(млрд|млн|тыс)?", text.replace("\xa0", " "))
    if not match:
        return 0
    number = float(match.group(1).replace(" ", "").replace(",", "."))
    scale = {"млрд": 1_000_000_000, "млн": 1_000_000, "тыс": 1000}.get(
        match.group(2) or "", 1)
    return int(round(number * scale))


def scalar(head: str, key: str) -> str:
    match = re.search(r'(?m)^%s:\s*"?(.*?)"?\s*$' % re.escape(key), head)
    return match.group(1) if match else ""


def parse_list(head: str, key: str, fields: tuple[str, ...]) -> list[dict]:
    """Список блоков вида `key:` -> `  - field: value`. Формат печатаем сами."""
    start = re.search(r"(?m)^%s:\s*$" % re.escape(key), head)
    if not start:
        return []
    rest = head[start.end():]
    stop = re.search(r"(?m)^[a-z_]+:", rest)
    block = rest[: stop.start()] if stop else rest
    rows, current = [], None
    for line in block.splitlines():
        item = re.match(r"\s+-\s+([a-z_]+):\s*(.*)$", line)
        if item:
            if current:
                rows.append(current)
            current = {}
            name, value = item.group(1), item.group(2)
        else:
            more = re.match(r"\s+([a-z_]+):\s*(.*)$", line)
            if not more or current is None:
                continue
            name, value = more.group(1), more.group(2)
        value = value.strip()
        if value.startswith('"') and value.endswith('"'):
            try:
                value = json.loads(value)
            except Exception:
                value = value.strip('"')
        if current is not None and name in fields:
            current[name] = value
    if current:
        rows.append(current)
    return rows


def facts_from(page: Path) -> dict | None:
    text = page.read_text(encoding="utf-8", errors="replace")
    if not text.startswith("---"):
        return None
    head = text.split("---", 2)[1]
    name = scalar(head, "club_name")
    if not name:
        return None

    squad = []
    for row in parse_list(head, "squad",
                          ("name", "position", "position_short", "age", "value")):
        age = row.get("age") or ""
        squad.append({
            "name": row.get("name") or "",
            "position": row.get("position") or "",
            "position_short": row.get("position_short") or "",
            "age": int(age) if str(age).isdigit() else None,
            "value": parse_money(row.get("value") or ""),
            "value_display": row.get("value") or "",
        })

    transfers = parse_list(head, "club_transfers",
                           ("player", "slug", "direction", "other_club", "fee"))
    size = scalar(head, "squad_size")
    return {
        "name": name,
        "league_id": scalar(head, "league_id"),
        "league_ru": scalar(head, "league"),
        "squad_size": int(size) if size.isdigit() else len(squad),
        "average_age": scalar(head, "average_age"),
        "squad_value": scalar(head, "squad_value"),
        "average_value": scalar(head, "average_value"),
        "squad_value_eur": int(scalar(head, "squad_value_eur") or 0),
        "squad": squad,
        "transfers": transfers,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--save", action="store_true")
    parser.add_argument("--show", type=int, default=1,
                        help="сколько готовых текстов показать целиком")
    args = parser.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")

    pages = sorted(CLUBS_DIR.glob("*/index.md"))
    print("\n=== ТЕКСТ КЛУБНЫХ СТРАНИЦ ===")
    print("  страниц: %d" % len(pages))

    plan, shown = [], 0
    for page in pages:
        facts = facts_from(page)
        if not facts:
            print("  пропуск: %s — шапка не разобрана" % page.parent.name)
            continue
        body = club_prose.build(facts)
        text = page.read_text(encoding="utf-8", errors="replace")
        head = text.split("---", 2)[1]
        was = len(text.split("---", 2)[2].split())
        new_text = "---" + head + "---\n\n" + "\n\n".join(body) + "\n"
        plan.append({"page": page.parent.name, "was": was,
                     "now": len(" ".join(body).split()), "_text": new_text})
        if shown < args.show:
            print("\n--- %s ---\n%s" % (page.parent.name, "\n\n".join(body)))
            shown += 1

    if not plan:
        print("  нечего писать\n")
        return 0

    was = sum(item["was"] for item in plan)
    now = sum(item["now"] for item in plan)
    short = len([item for item in plan if item["now"] < 200])
    print("\n  слов было %d (в среднем %d), стало %d (в среднем %d)"
          % (was, was // len(plan), now, now // len(plan)))
    print("  короче 200 слов осталось: %d" % short)

    if not args.save:
        print("\n  это показ; чтобы применить — тот же вызов с --save\n")
        return 0

    stamp = datetime.now(timezone.utc).astimezone().strftime("%Y%m%d_%H%M%S")
    backup = BACKUPS / ("%s_CLUB_PROSE" % stamp)
    backup.mkdir(parents=True, exist_ok=True)
    for item in plan:
        source = CLUBS_DIR / item["page"] / "index.md"
        (backup / item["page"]).mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, backup / item["page"] / "index.md")
        source.write_text(item.pop("_text"), encoding="utf-8")

    REPORTS.mkdir(parents=True, exist_ok=True)
    report = REPORTS / ("%s_CLUB_PROSE.json" % stamp)
    report.write_text(json.dumps({
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "backup": str(backup), "words_before": was, "words_after": now,
        "pages": plan,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print("\n  переписано страниц: %d" % len(plan))
    print("  копия: %s" % backup)
    print("  отчёт: %s\n" % report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
