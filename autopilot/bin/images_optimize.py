"""
PROMYACHIK - ПЕРЕЖАТИЕ ЛОГОТИПОВ КЛУБОВ

Зачем. На главной 126 логотипов грузятся сразу, без отсрочки, и весят вместе
1654 КБ. Отдельные экземпляры доходят до 141 КБ - при том, что показываются
размером 34-54 пикселя. Дело не в разрешении: файлы и так 150x150. Дело в
кодировании - они лежат 32-битными RGBA без палитры, то есть почти как есть.

Друг Дмитрия пожаловался, что сайт долго открывается. Хостинг тут ни при чём:
DNS отвечает за 4 мс, соединение ставится за 25 мс. Полтора мегабайта значков
- вот что он ждал.

ПОЧЕМУ НЕ WEBP

Соблазн велик, но смена расширения тянет за собой правку путей в шаблонах, в
данных и в самом движке 3.4, который эти файлы называет и скачивает.
Замороженного движка это касается напрямую, а выигрыш почти тот же: логотип
клуба - плоская графика, палитра сжимает её не хуже. Поэтому имя файла
остаётся прежним, меняется только содержимое. Ни одной ссылки править не
нужно, откат - копирование папки обратно.

КАК СОХРАНЯЕТСЯ КАЧЕСТВО

Для каждого файла считаются два варианта: честное пережатие без потерь и
палитра на 256 цветов. У второго измеряется средняя ошибка по видимым
пикселям, и он берётся, только если ошибка ниже порога. Крест с плавным
переходом палитру не переживёт - такой файл останется несжатым, и это
правильно: значок клуба узнают по форме и цвету.

Файл заменяется, только если стал меньше заметно - иначе смысла нет.

Запускается без ключей - показывает, что сделал бы. Меняет с --save,
предварительно сложив копию в patch-backups.
"""
from __future__ import annotations

import argparse
import io
import json
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

from PIL import Image, ImageChops, ImageStat

BIN = Path(__file__).resolve().parent
sys.path.insert(0, str(BIN))
from transfer_discovery import ACTIVE_PROJECT, PARSER_ROOT  # noqa: E402

BACKUPS = PARSER_ROOT.parent / "patch-backups"
REPORTS = PARSER_ROOT.parent / "reports"

# Только логотипы. Портреты - фотографии, палитра их испортит, им нужен
# отдельный разговор про формат.
TARGETS = [
    ACTIVE_PROJECT / "static" / "images" / "clubs" / "api" / "rendered",
    ACTIVE_PROJECT / "static" / "images" / "clubs" / "api",
]

# Средняя ошибка на канал, выше которой палитра считается порчей. Три единицы
# из 255 - это примерно предел, за которым разница видна на плоской заливке.
MAX_ERROR = 3.0

# Экономия меньше этой доли не стоит перезаписи файла.
MIN_GAIN = 0.15

# Файлы меньше этого размера уже сжаты как надо: логотип 150x150 в палитре
# весит 3-7 КБ. Проверять их на каждом такте незачем - именно этот порог
# превращает шаг из «пережать всё» в «пережать только что скачанное».
SKIP_BELOW = 12 * 1024


def encode(image: Image.Image, palette: bool) -> bytes:
    buffer = io.BytesIO()
    if palette:
        image.quantize(colors=256, method=Image.Quantize.FASTOCTREE).save(
            buffer, format="PNG", optimize=True)
    else:
        image.save(buffer, format="PNG", optimize=True)
    return buffer.getvalue()


def error_of(original: Image.Image, data: bytes) -> float:
    """Средняя разница по видимым пикселям, 0-255 на канал."""
    candidate = Image.open(io.BytesIO(data)).convert("RGBA")
    diff = ImageChops.difference(original.convert("RGB"), candidate.convert("RGB"))
    alpha = original.getchannel("A")
    stat = ImageStat.Stat(diff, mask=alpha)
    return max(stat.mean) if stat.mean else 0.0


def best_for(path: Path) -> tuple[bytes, str, float] | None:
    original = Image.open(path).convert("RGBA")
    lossless = encode(original, palette=False)
    variants = [(lossless, "без потерь", 0.0)]

    paletted = encode(original, palette=True)
    err = error_of(original, paletted)
    if err <= MAX_ERROR:
        variants.append((paletted, "палитра", err))

    data, how, err = min(variants, key=lambda item: len(item[0]))
    if len(data) >= path.stat().st_size * (1 - MIN_GAIN):
        return None
    return data, how, err


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--save", action="store_true",
                        help="перезаписать файлы; без ключа только показывает")
    parser.add_argument("--top", type=int, default=12,
                        help="сколько самых тяжёлых показать в отчёте")
    args = parser.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")

    files: list[Path] = []
    for directory in TARGETS:
        if directory.exists():
            files.extend(sorted(p for p in directory.glob("*.png") if p.is_file()))

    print("\n=== ПЕРЕЖАТИЕ ЛОГОТИПОВ ===")
    print("  файлов: %d" % len(files))

    plan: list[dict] = []
    skipped_quality = 0
    for path in files:
        if path.stat().st_size < SKIP_BELOW:
            continue
        try:
            result = best_for(path)
        except Exception as error:
            print("  пропуск %s: %s" % (path.name, str(error)[:60]))
            continue
        if result is None:
            continue
        data, how, err = result
        was = path.stat().st_size
        plan.append({"file": str(path.relative_to(ACTIVE_PROJECT)),
                     "was": was, "now": len(data), "how": how,
                     "error": round(err, 2), "_data": data})
        if how == "без потерь":
            skipped_quality += 1

    if not plan:
        print("  сжимать нечего\n")
        return 0

    was = sum(item["was"] for item in plan)
    now = sum(item["now"] for item in plan)
    plan.sort(key=lambda item: item["was"] - item["now"], reverse=True)
    print("  выигрыш: %.1f МБ -> %.1f МБ (минус %d%%) на %d файлах"
          % (was / 1048576, now / 1048576, 100 - now * 100 // was, len(plan)))
    print("  палитра не подошла по качеству: %d" % skipped_quality)
    print("\n  крупнейшие:")
    for item in plan[: args.top]:
        print("    %6d -> %5d КБ  %-10s ошибка %.2f  %s"
              % (item["was"] // 1024, item["now"] // 1024, item["how"],
                 item["error"], Path(item["file"]).name[:44]))

    if not args.save:
        print("\n  это показ; чтобы применить — тот же вызов с --save\n")
        return 0

    stamp = datetime.now(timezone.utc).astimezone().strftime("%Y%m%d_%H%M%S")
    backup = BACKUPS / ("%s_LOGO_OPTIMIZE" % stamp)
    for directory in TARGETS:
        if directory.exists():
            shutil.copytree(directory, backup / directory.name,
                            dirs_exist_ok=True)

    for item in plan:
        (ACTIVE_PROJECT / item["file"]).write_bytes(item.pop("_data"))

    REPORTS.mkdir(parents=True, exist_ok=True)
    report = REPORTS / ("%s_LOGO_OPTIMIZE.json" % stamp)
    report.write_text(json.dumps({
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "backup": str(backup),
        "was_bytes": was, "now_bytes": now,
        "files": plan,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print("\n  переписано файлов: %d" % len(plan))
    print("  копия: %s" % backup)
    print("  отчёт: %s\n" % report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
