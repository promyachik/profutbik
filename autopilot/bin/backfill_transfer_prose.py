"""
PROMYACHIK - ДОПИСАТЬ НЕДОСТАЮЩИЕ РАЗДЕЛЫ НА СТРАНИЦАХ ТРАНСФЕРОВ

Дописывает то, чего на странице нет, и не трогает то, что есть. Материал -
transfer_prose, то есть наши же страницы клубов и данные графика. Сеть не
используется вообще.

ЧТО ИМЕННО ДОПИСЫВАЕТСЯ

    "Что получает клуб"   состав нового клуба и ссылка на его страницу
    роль в составе        место по стоимости, конкуренты на позиции, возраст
    путь по клубам        оценка игрока на каждом шаге карьеры

Раздел, который на странице уже есть, пропускается: второй "Что получает клуб"
хуже, чем ни одного. Проверка по характерной фразе, а не по длине.

КУДА ВСТАВЛЯЕТСЯ

Перед подписью источника. Она обязана остаться последней строкой: по ней
читатель понимает, откуда факты, и уводить её в середину значит ломать смысл
страницы.

Шапка не трогается ни в одном байте - её пишет движок 3.4.

Запускается без ключей - показывает. Меняет с --save, сложив копии в
patch-backups.
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
import transfer_prose  # noqa: E402

TRANSFERS_DIR = ACTIVE_PROJECT / "content" / "transfers"
BACKUPS = PARSER_ROOT.parent / "patch-backups"
REPORTS = PARSER_ROOT.parent / "reports"

# По этим приметам понимаем, что раздел уже написан движком.
MARKS = {
    "club": ("В составе клуба", "Что получает клуб"),
    "role": ("рейтинге стоимости состава",),
    "career": ("Как менялась оценка",),
}


def scalar(head: str, key: str) -> str:
    found = re.search(r'(?m)^%s:\s*"?(.*?)"?\s*$' % re.escape(key), head)
    return found.group(1) if found else ""


def split_tail(body: str) -> tuple[str, str]:
    """Отделяет подпись источника: она должна остаться в самом низу."""
    match = None
    for match in re.finditer(r"(?m)^---\s*$", body):
        pass
    if match and "Источник" in body[match.end():]:
        return body[: match.start()].rstrip("\n"), body[match.start():]
    return body.rstrip("\n"), ""


def sections_for(page: Path) -> list[str]:
    text = page.read_text(encoding="utf-8", errors="replace")
    if not text.startswith("---"):
        return []
    head, body = text.split("---", 2)[1], text.split("---", 2)[2]
    player = scalar(head, "player") or scalar(head, "player_name")
    to_club = scalar(head, "to_club_name") or scalar(head, "to_name")
    if not player:
        return []

    added: list[str] = []
    club = transfer_prose.club_by_name(to_club) if to_club else None

    if club and not any(m in body for m in MARKS["club"]):
        paragraph = transfer_prose.club_paragraph(club)
        if paragraph:
            added.append("## Что получает клуб\n\n" + paragraph)

    if club and not any(m in body for m in MARKS["role"]):
        paragraph = transfer_prose.role_paragraph(
            player, club, scalar(head, "position_ru"),
            scalar(head, "age_at_transfer") or scalar(head, "age"))
        if paragraph:
            if added:
                added[-1] += "\n\n" + paragraph
            else:
                added.append("## Роль в новом составе\n\n" + paragraph)

    if not any(m in body for m in MARKS["career"]):
        row = transfer_prose.chart().get(page.parent.name)
        if row:
            paragraph = transfer_prose.career_paragraph(row, player)
            if paragraph:
                added.append("## Путь по клубам\n\n" + paragraph)
    return added


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--save", action="store_true")
    parser.add_argument("--show", type=int, default=2)
    args = parser.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")

    pages = sorted(TRANSFERS_DIR.glob("*/index.md"))
    print("\n=== РАЗДЕЛЫ СТРАНИЦ ТРАНСФЕРОВ ===")
    print("  страниц: %d" % len(pages))
    print("  клубов с составом у нас: %d" % len(transfer_prose.clubs()))
    print("  игроков с графиком: %d" % len(transfer_prose.chart()))

    plan, shown = [], 0
    for page in pages:
        added = sections_for(page)
        if not added:
            continue
        text = page.read_text(encoding="utf-8", errors="replace")
        head, body = text.split("---", 2)[1], text.split("---", 2)[2]
        top, tail = split_tail(body)
        new_body = top + "\n\n" + "\n\n".join(added) + "\n"
        if tail:
            new_body += "\n" + tail.lstrip("\n")
        plan.append({"page": page.parent.name,
                     "was": len(body.split()), "now": len(new_body.split()),
                     "added": len(added),
                     "_text": "---" + head + "---" + new_body})
        if shown < args.show:
            print("\n--- %s ---\n%s" % (page.parent.name, "\n\n".join(added)))
            shown += 1

    if not plan:
        print("\n  дописывать нечего\n")
        return 0

    was = sum(item["was"] for item in plan)
    now = sum(item["now"] for item in plan)
    print("\n  затронуто страниц: %d из %d" % (len(plan), len(pages)))
    print("  слов было %d (в среднем %d), стало %d (в среднем %d)"
          % (was, was // len(plan), now, now // len(plan)))

    if not args.save:
        print("\n  это показ; чтобы применить — тот же вызов с --save\n")
        return 0

    stamp = datetime.now(timezone.utc).astimezone().strftime("%Y%m%d_%H%M%S")
    backup = BACKUPS / ("%s_TRANSFER_PROSE" % stamp)
    for item in plan:
        source = TRANSFERS_DIR / item["page"] / "index.md"
        (backup / item["page"]).mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, backup / item["page"] / "index.md")
        source.write_text(item.pop("_text"), encoding="utf-8")

    REPORTS.mkdir(parents=True, exist_ok=True)
    report = REPORTS / ("%s_TRANSFER_PROSE.json" % stamp)
    report.write_text(json.dumps({
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "backup": str(backup), "words_before": was, "words_after": now,
        "pages": plan,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print("\n  дописано страниц: %d" % len(plan))
    print("  копия: %s" % backup)
    print("  отчёт: %s\n" % report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
