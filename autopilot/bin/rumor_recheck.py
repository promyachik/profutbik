"""
PROMYACHIK TRANSFER AUTOPILOT - ПЕРЕПРОВЕРКА ОПУБЛИКОВАННЫХ СЛУХОВ

Шаг, который был описан в шапке rumor_publisher.py с самого начала, но так и
не построен:

    "Каждый прогон перепроверяет все записи в состоянии PUBLISHED_AS_RUMOR
     через состав клуба назначения. Как только игрок там появился, сделка
     считается закрытой."

Пока его не было, слух жил вечно. Дмитрий поймал это на живом сайте: Ibrahima
Konate висел слухом про "Реал", отыграв к тому моменту четыре тура в Ла Лиге.
Проверка нашла ещё четверых в том же состоянии - Кукурелью, Бернарду Силву,
Гонсалу Рамуша и Эллиота Андерсона. Пять из двенадцати слухов на главной были
не слухами, а свершившимися переходами, и у всех пяти на нашем же сайте лежала
страница трансфера. Сайт спорил сам с собой.

ПОЧЕМУ ЭТО НЕ ГРУЗИТ СИСТЕМУ

Состав клуба назначения берётся не из сети, а из наших же страниц клубов:
4179 игроков, 148 клубов, у каждого записан текущий клуб. Полный проход по
всем слухам - 0.13 секунды и ноль запросов.

Через API та же работа стоила бы около 210 запросов: /club/<id>/squad отдаёт
только playerId без имён, и на каждого игрока нужен отдельный вызов. Поэтому
сеть здесь не используется вовсе. Если игрока в локальном индексе нет, запись
просто не трогается - молчание безопаснее догадки.

ДВЕ ВЕТКИ

    страница трансфера уже есть  -> слух снимается, адрес перенаправляется
    страницы трансфера ещё нет   -> запись помечается для движка, слух остаётся

Вторая ветка намеренно не убирает слух: снять материал, не поставив на его
место трансфер, значит оставить на сайте дыру. Пусть лучше день повисит
устаревший слух, чем страница исчезнет в никуда.

УДАЛЕНИЕ И РЕДИРЕКТ

Страница слуха не стирается молча: сначала копия уходит в patch-backups,
потом на странице трансфера появляется alias со старого адреса. Hugo делает
из него редирект, и проиндексированный адрес не превращается в 404 - это
важно отдельно, потому что с индексацией у сайта и без того непорядок.

Запускается без ключей - только показывает, что сделал бы. Меняет что-либо
исключительно с --save.
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
from transfer_discovery import ACTIVE_PROJECT, PARSER_ROOT, RECORDS_DIR  # noqa: E402
import transfer_enrichment as te  # noqa: E402
from rumor_publisher import _front_matter, HOMEPAGE_JSON, RUMORS_DIR  # noqa: E402

TRANSFERS_DIR = ACTIVE_PROJECT / "content" / "transfers"
BACKUPS = PARSER_ROOT.parent / "patch-backups"
REPORTS = PARSER_ROOT.parent / "reports"


def now_stamp() -> str:
    return datetime.now(timezone.utc).astimezone().strftime("%Y%m%d_%H%M%S")


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def same_club(left: str, right: str) -> bool:
    """Один ли это клуб.

    Названия приходят в разном виде: "Arsenal" и "Arsenal FC", "Atletico
    Madrid" и "Atletico de Madrid". Сравниваем нормализованные строки и
    допускаем вложенность одной в другую - но только по границам слов, иначе
    "Real Madrid" совпадёт с "Real Madrid Castilla".
    """
    a, b = te.normalize(left or ""), te.normalize(right or "")
    if not a or not b:
        return False
    if a == b:
        return True
    aw, bw = a.split(), b.split()
    return aw[: len(bw)] == bw or bw[: len(aw)] == aw


def transfer_page_for(player: str, to_club: str) -> str | None:
    """Slug нашей страницы трансфера про этот же переход, если она есть.

    Клуб назначения в двух разделах назван по-разному: у слухов это
    `to_club`, у трансферов - `to_club_name`. Разница историческая, сводить
    её задним числом дороже, чем прочитать оба поля.
    """
    if not TRANSFERS_DIR.exists():
        return None
    wanted = te.normalize(player)
    for page in sorted(TRANSFERS_DIR.glob("*/index.md")):
        fm = _front_matter(page)
        if te.normalize(fm.get("player") or "") != wanted:
            continue
        club = fm.get("to_club_name") or fm.get("to_club") or ""
        if same_club(club, to_club):
            return page.parent.name
    return None


def current_club(player: str) -> str | None:
    """Клуб игрока по нашему индексу составов. Однофамильцы -> None."""
    row = te.resolve_local_player(player or "")
    if not row or "__ambiguous__" in row:
        return None
    return row.get("club") or None


def add_alias(slug: str, old_url: str) -> bool:
    """Прописывает редирект со старого адреса слуха на страницу трансфера."""
    page = TRANSFERS_DIR / slug / "index.md"
    text = page.read_text(encoding="utf-8")
    if old_url in text:
        return False
    if not text.startswith("---"):
        return False
    head, body = text[3:].split("---", 1)
    match = re.search(r'(?m)^aliases:\s*\[(.*?)\]\s*$', head)
    if match:
        inside = match.group(1).strip()
        merged = (inside + ", " if inside else "") + '"%s"' % old_url
        head = head[: match.start()] + 'aliases: [%s]' % merged + head[match.end():]
    else:
        head = head.rstrip("\n") + '\naliases: ["%s"]\n' % old_url
    page.write_text("---" + head + "---" + body, encoding="utf-8")
    return True


def records_by_slug() -> dict[str, Path]:
    """Записи очереди, у которых есть опубликованная страница слуха."""
    out: dict[str, Path] = {}
    for path in sorted(RECORDS_DIR.glob("*.json")):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            continue
        slug = data.get("rumor_slug") or data.get("rumor_slug_override")
        if slug:
            out[slug] = path
    return out


def mark_record(path: Path, state: str, detail: str) -> None:
    data = json.loads(path.read_text(encoding="utf-8"))
    data["pipeline_state"] = state
    data["block_reason"] = ""
    data["block_detail"] = detail
    data["rumor_rechecked_at"] = now_iso()
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n",
                    encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--save", action="store_true",
                        help="применить изменения; без ключа только показывает")
    args = parser.parse_args()

    sys.stdout.reconfigure(encoding="utf-8")
    print("\n=== ПЕРЕПРОВЕРКА СЛУХОВ ===")
    index = te.local_player_index()
    print("  индекс составов: %d игроков, ноль запросов в сеть" % len(index))

    records = records_by_slug()
    retired: list[dict] = []
    promoted: list[dict] = []
    dropped_rows: list[dict] = []

    # 1. Страницы раздела "Слухи".
    for page in sorted(RUMORS_DIR.glob("*/index.md")):
        slug = page.parent.name
        fm = _front_matter(page)
        player, to_club = fm.get("player") or "", fm.get("to_club") or ""
        if not player or not to_club:
            continue
        club = current_club(player)
        if not club or not same_club(club, to_club):
            continue

        target = transfer_page_for(player, to_club)
        item = {"player": player, "to_club": to_club, "rumor": slug,
                "transfer": target}
        if target:
            retired.append(item)
            print("  СНЯТЬ  %s: уже в составе %s, трансфер на месте -> /transfers/%s/"
                  % (player, club, target))
        else:
            promoted.append(item)
            print("  В ОЧЕРЕДЬ  %s: уже в составе %s, страницы трансфера нет"
                  % (player, club))

    # 2. Строки на главной, ведущие в раздел трансферов. Пересборка блока их
    #    намеренно сохраняет, поэтому снимать приходится отдельно.
    homepage = json.loads(HOMEPAGE_JSON.read_text(encoding="utf-8"))
    retired_slugs = {item["rumor"] for item in retired}
    keep = []
    for row in homepage.get("rumors") or []:
        url = str(row.get("url") or "")
        if url.startswith("rumors/"):
            # Строку снятого слуха убираем здесь же. Пересборка блока из
            # страниц сделала бы это сама, но только на следующем такте, а до
            # него на главной висела бы ссылка в никуда.
            if str(row.get("slug") or "") in retired_slugs:
                dropped_rows.append({"player": row.get("player"), "url": url})
                continue
            keep.append(row)
            continue
        club = current_club(row.get("player") or "")
        if club and same_club(club, row.get("to_name") or ""):
            dropped_rows.append({"player": row.get("player"), "url": url})
            print("  СНЯТЬ СТРОКУ  %s: уже в составе %s, строка вела в %s"
                  % (row.get("player"), club, url))
            continue
        keep.append(row)

    total = len(retired) + len(promoted) + len(dropped_rows)
    if not total:
        print("\n  устаревших слухов нет\n")
        return 0

    if not args.save:
        print("\n  это показ; чтобы применить — тот же вызов с --save\n")
        return 0

    stamp = now_stamp()
    backup = BACKUPS / ("%s_RUMOR_RECHECK" % stamp)
    backup.mkdir(parents=True, exist_ok=True)
    shutil.copy2(HOMEPAGE_JSON, backup / HOMEPAGE_JSON.name)

    for item in retired:
        src = RUMORS_DIR / item["rumor"]
        shutil.copytree(src, backup / "rumors" / item["rumor"])
        add_alias(item["transfer"], "/rumors/%s/" % item["rumor"])
        shutil.rmtree(src)
        record = records.get(item["rumor"])
        if record:
            mark_record(record, "RUMOR_CAME_TRUE",
                        "игрок в составе %s; слух снят, адрес ведёт на "
                        "/transfers/%s/" % (item["to_club"], item["transfer"]))

    for item in promoted:
        record = records.get(item["rumor"])
        if record:
            mark_record(record, "CONFIRMED_TO_TRANSFER",
                        "игрок уже в составе %s — слух подтвердился, нужен "
                        "полный трансфер" % item["to_club"])

    if dropped_rows:
        homepage["rumors"] = keep
        HOMEPAGE_JSON.write_text(
            json.dumps(homepage, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8")

    REPORTS.mkdir(parents=True, exist_ok=True)
    report = REPORTS / ("%s_RUMOR_RECHECK.json" % stamp)
    report.write_text(json.dumps({
        "generated_at": now_iso(),
        "backup": str(backup),
        "retired": retired,
        "promoted": promoted,
        "dropped_rows": dropped_rows,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print("\n  снято слухов: %d, в очередь на трансфер: %d, снято строк: %d"
          % (len(retired), len(promoted), len(dropped_rows)))
    print("  копия: %s" % backup)
    print("  отчёт: %s\n" % report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
