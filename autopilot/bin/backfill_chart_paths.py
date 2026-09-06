"""
PF527B — НАСТОЯЩИЙ ПУТЬ ИГРОКА НА УЖЕ ОПУБЛИКОВАННЫХ ГРАФИКАХ

Что было. Точки графика собирались так: все, кроме последней, приписывались
клубу «откуда», последняя — клубу «куда». Путь у любого игрока состоял ровно
из двух клубов, даже если он сменил пять. Дмитрий заметил это на Аханоре: на
графике «Аталанта → Кристал Пэлас», а «Дженоа», где он играл между ними, нет.

Причина глубже отрисовки. Обогащение брало у Transfermarkt только три поля —
пик, предыдущую и текущую оценку, — и в записи оказывалось две-три точки.
Полная история лежит по другому адресу и содержит клуб на каждой дате: у того
же Аханора там семь точек и три клуба.

Публикация новых трансферов исправлена в publisher.py. Этот скрипт пересобирает
тех, кто опубликован раньше.

Чего скрипт НЕ делает: не подменяет последний клуб на клуб назначения. Если
Transfermarkt ещё не переоценил игрока после перехода, последняя точка честно
остаётся за прежним клубом — это оценка того периода, а не сегодняшнего дня.
Клуб назначения виден в шапке статьи, там ему и место.

Запуск:
    python backfill_chart_paths.py               показать, что изменится
    python backfill_chart_paths.py --save        записать
    python backfill_chart_paths.py --limit 5     первые пять, для пробы
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from paths import SITE  # noqa: E402
import market_value_chart as mvc  # noqa: E402

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

CHART_JS = SITE / "static" / "js" / "transfer-player-market-value-chart.js"
SINGLE = SITE / "layouts" / "transfers" / "single.html"


def load_players(text: str) -> tuple[list[dict], tuple[int, int]]:
    found = re.search(r"(?m)^(\s*const PLAYERS = )(\[.*\])(;\s*)$", text)
    if not found:
        raise SystemExit("не нашёл массив PLAYERS")
    return json.loads(found.group(2)), (found.start(2), found.end(2))


def slug_of(player: dict) -> str:
    for path in player.get("paths") or []:
        match = re.match(r"^/transfers/([^/]+)/", path)
        if match:
            return match.group(1)
    return ""


def rebuild(slug: str) -> list[dict] | None:
    """Точки по полной истории. None — данных не хватило, запись не трогаем."""
    try:
        meta = mvc.transfer_meta(slug)
    except Exception:  # noqa: BLE001
        return None
    if not meta.get("tm_id"):
        return None

    history = mvc.market_history(str(meta["tm_id"]))
    if len(history) < 2:
        return None

    chosen = mvc.select_points(history)
    labels = mvc.label_points(chosen)
    index = mvc.club_index()
    clubs: dict[str, dict] = {}
    points = []
    for row, label in zip(chosen, labels):
        value_label = mvc.money_label(row["compact"])
        if not value_label:
            continue
        club_id = row["club_id"]
        # У части оценок клуб не проставлен вовсе (club_id пустой или «0»).
        # Такая точка дала бы на графике кружок с подписью «Клуб 0» и запрос
        # за несуществующим гербом. Лучше без неё.
        if not club_id or club_id == "0":
            continue
        if club_id not in clubs:
            clubs[club_id] = mvc.resolve_club(club_id, history, index)
        points.append({"label": label, "value_label": value_label,
                       "value": round(row["value"] / 1_000_000, 2),
                       "club": clubs[club_id]})
    return points if len(points) >= 2 else None


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--save", action="store_true")
    parser.add_argument("--limit", type=int, default=0)
    args = parser.parse_args()

    text = CHART_JS.read_text(encoding="utf-8")
    players, span = load_players(text)
    print("Игроков в объекте: %d" % len(players))

    grown: list[str] = []
    same: list[str] = []
    skipped: list[str] = []
    touched = 0

    for player in players:
        if args.limit and touched >= args.limit:
            break
        slug = slug_of(player)
        if not slug:
            skipped.append("%s: не разобрал адрес" % player.get("name"))
            continue

        was_clubs = len({(p.get("club") or {}).get("name") for p in player.get("points") or []})
        was_points = len(player.get("points") or [])

        try:
            points = rebuild(slug)
        except Exception as error:  # noqa: BLE001
            skipped.append("%s: %s" % (player.get("name"), str(error)[:70]))
            continue
        touched += 1

        if not points:
            skipped.append("%s: истории мало" % player.get("name"))
            continue

        now_clubs = len({p["club"]["name"] for p in points})

        # PF527B: не заменяем, если клубов в пути станет МЕНЬШЕ.
        # У девяти игроков Transfermarkt ещё не переоценил их после перехода,
        # и последняя точка истории честно принадлежит прежнему клубу — то
        # есть клуб назначения с графика исчез бы вовсе. Прежняя раскладка
        # «откуда → куда» для них хоть и грубая, но полнее. Пусть остаются
        # как были: правка не должна никому делать хуже.
        if now_clubs < was_clubs:
            same.append("%s (клубов стало бы меньше: %d→%d, оставил как было)"
                        % (player.get("name"), was_clubs, now_clubs))
            continue

        if now_clubs > was_clubs or len(points) > was_points:
            grown.append("%-26s точек %d→%d, клубов %d→%d  (%s)"
                         % (player.get("name"), was_points, len(points),
                            was_clubs, now_clubs,
                            " → ".join(dict.fromkeys(p["club"]["name"] for p in points))))
            player["points"] = points
        else:
            same.append(player.get("name"))

    print("\nПуть стал полнее: %d" % len(grown))
    for line in grown:
        print("  " + line)
    print("\nБез изменений: %d" % len(same))
    print("Пропущено: %d" % len(skipped))
    for line in skipped:
        print("  " + line)

    if not args.save:
        print("\nСухой прогон. Записать: --save")
        return 0
    if not grown:
        print("\nМенять нечего.")
        return 0

    payload = json.dumps(players, ensure_ascii=False, separators=(", ", ": "))
    CHART_JS.write_text(text[:span[0]] + payload + text[span[1]:], encoding="utf-8")
    print("\nЗаписано: %s" % CHART_JS)

    single = SINGLE.read_text(encoding="utf-8")
    updated, count = re.subn(
        r"(transfer-player-market-value-chart\.js\?v=)[^\"']+", r"\g<1>pf527b", single)
    if count:
        SINGLE.write_text(updated, encoding="utf-8")
        print("Токен графика обновлён: pf527b")
    else:
        print("! Токен не найден — проверить вручную")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
