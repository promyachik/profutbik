"""
PF523A — ЛОГОТИПЫ КЛУБОВ В СТАРЫХ ОБЪЕКТАХ ГРАФИКА

На графике стоимости у каждой точки стоит эмблема клуба, а если её нет —
буква клуба в золотом кружке. Заглушка сделана правильно и нужна: клубы вроде
«Десны» или «Синт-Трёйдена» в наши восемь лиг не входят, эмблемы у нас нет и
взять её неоткуда.

Беда в том, что заглушка вылезала и там, где эмблема есть. Пример — страница
Кукурельи: «Барселона», «Реал», «Брайтон» показывались буквами, хотя их гербы
лежат у нас в static/images/clubs.

Причина: записи, сделанные до движка 3.4, содержат `api_id` клуба, но не
содержат поля `logo`, а отрисовка смотрит только на `logo`. Новые записи от
автопилота его проставляют, старые — нет.

Скрипт проходит по массиву PLAYERS и дописывает `logo` там, где клуб опознан:
сперва по `api_id` в справочнике клубов, затем по точному совпадению названия.
Ничего не удаляет и не переписывает: точки, у которых логотипа не нашлось,
остаются с буквой — так и задумано.

Запуск:
    python backfill_chart_logos.py            показать, что изменится
    python backfill_chart_logos.py --save     записать
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from paths import SITE  # noqa: E402

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

CHART_JS = SITE / "static" / "js" / "transfer-player-market-value-chart.js"
CLUB_LOGOS = SITE / "data" / "club-logos.json"
SINGLE = SITE / "layouts" / "transfers" / "single.html"


def normalize(value: str) -> str:
    text = unicodedata.normalize("NFD", str(value or ""))
    text = "".join(ch for ch in text if unicodedata.category(ch) != "Mn")
    text = text.lower().replace("&", " ").replace(".", " ").replace("-", " ")
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9 ]", " ", text)).strip()


def load_players(text: str) -> tuple[list[dict], tuple[int, int]]:
    found = re.search(r"(?m)^(\s*const PLAYERS = )(\[.*\])(;\s*)$", text)
    if not found:
        raise SystemExit("не нашёл массив PLAYERS в %s" % CHART_JS)
    return json.loads(found.group(2)), (found.start(2), found.end(2))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--save", action="store_true")
    args = parser.parse_args()

    directory = json.loads(CLUB_LOGOS.read_text(encoding="utf-8"))
    clubs = directory.get("clubs") or {}
    by_id = {str(k): v for k, v in clubs.items()}
    by_name: dict[str, dict] = {}
    for club in clubs.values():
        for variant in (club.get("name"), club.get("configured_name")):
            if variant:
                by_name.setdefault(normalize(variant), club)

    text = CHART_JS.read_text(encoding="utf-8")
    players, span = load_players(text)

    fixed_id: list[str] = []
    fixed_name: list[str] = []
    left: dict[str, int] = {}

    for player in players:
        for point in player.get("points") or []:
            club = point.get("club") or {}
            if club.get("logo"):
                continue

            source = None
            how = None
            api_id = club.get("api_id")
            if api_id is not None:
                source = by_id.get(str(api_id))
                how = "по id"
            if source is None or not source.get("logo"):
                found = by_name.get(normalize(club.get("name") or ""))
                if found and found.get("logo"):
                    source, how = found, "по названию"

            if source and source.get("logo"):
                club["logo"] = source["logo"]
                line = "%-28s %-26s %s" % (player.get("name"), club.get("name"), how)
                (fixed_id if how == "по id" else fixed_name).append(line)
            else:
                left[club.get("name") or "?"] = left.get(club.get("name") or "?", 0) + 1

    print("Игроков в объекте: %d" % len(players))
    print("\nЛоготип найден по id: %d" % len(fixed_id))
    for line in fixed_id:
        print("  " + line)
    print("\nЛоготип найден по названию: %d" % len(fixed_name))
    for line in fixed_name:
        print("  " + line)
    print("\nОстаются с буквой — их эмблем у нас нет: %d точек" % sum(left.values()))
    for name, count in sorted(left.items(), key=lambda x: -x[1]):
        print("  %-30s %d" % (name, count))

    if not args.save:
        print("\nСухой прогон. Записать: --save")
        return 0
    if not (fixed_id or fixed_name):
        print("\nМенять нечего.")
        return 0

    payload = json.dumps(players, ensure_ascii=False, separators=(", ", ": "))
    CHART_JS.write_text(text[:span[0]] + payload + text[span[1]:], encoding="utf-8")
    print("\nЗаписано: %s" % CHART_JS)

    # Правило проекта: без нового токена браузер отдаст прежний скрипт, и
    # эмблемы не появятся, сколько ни обновляй.
    single = SINGLE.read_text(encoding="utf-8")
    updated, count = re.subn(
        r"(transfer-player-market-value-chart\.js\?v=)[^\"']+",
        r"\g<1>pf523a", single)
    if count:
        SINGLE.write_text(updated, encoding="utf-8")
        print("Токен графика в single.html обновлён: pf523a (%d мест)" % count)
    else:
        print("! Токен в single.html не найден — проверить вручную")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
