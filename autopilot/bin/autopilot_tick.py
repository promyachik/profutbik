"""
PROMYACHIK — ОДИН ТАКТ АВТОПИЛОТА

Задумано под запуск по расписанию: проснулся, опубликовал **один** трансфер,
вышел. Штучность здесь не от лени, а по делу:

- у трансфера пять обязательных частей, и при штучной публикации поломка
  видна сразу, а откатывается одна транзакция вместо десяти;
- домену несколько дней; сайт, получающий десятки страниц в час, для поиска
  выглядит свалкой, а не изданием.

Порядок внутри такта:
  1. разведка по лентам (если разрешена) — свежие переходы и слухи;
  2. обогащение — личность, портрет, стоимость, подтверждение по составу;
  3. сборка job для готовых записей;
  4. публикация ОДНОГО job через движок 3.4 с полной валидацией.

Ничего не публикует, если публиковать нечего: это нормальный исход такта.

    python autopilot_tick.py                 полный такт
    python autopilot_tick.py --no-discovery  только очередь, без лент
    python autopilot_tick.py --dry-run       ничего не менять
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

BIN = Path(__file__).resolve().parent
sys.path.insert(0, str(BIN))
from paths import PARSER_ROOT, ensure_dirs  # noqa: E402

RECORDS_DIR = PARSER_ROOT / "state" / "records"
JOBS_DIR = PARSER_ROOT / "jobs"
PUBLISHED_LOG = PARSER_ROOT / "state" / "published_jobs.json"


def run(module: str, *args: str) -> int:
    """Запуск соседнего модуля тем же интерпретатором."""
    command = [sys.executable, str(BIN / module), *args]
    print("  $ %s %s" % (module, " ".join(args)), flush=True)
    result = subprocess.run(command, cwd=str(BIN))
    return result.returncode


def published() -> set[str]:
    if PUBLISHED_LOG.exists():
        try:
            return set(json.loads(PUBLISHED_LOG.read_text(encoding="utf-8")))
        except Exception:
            return set()
    return set()


def remember(name: str) -> None:
    done = published()
    done.add(name)
    PUBLISHED_LOG.write_text(json.dumps(sorted(done), ensure_ascii=False, indent=1),
                             encoding="utf-8")


PACE_MINUTES = 30
MAX_PER_TICK = 4
LAST_PUBLISH = PARSER_ROOT / "state" / "last_publish.txt"


def _last_publish() -> "datetime | None":
    if not LAST_PUBLISH.exists():
        return None
    try:
        return datetime.fromisoformat(LAST_PUBLISH.read_text(encoding="utf-8").strip())
    except Exception:
        return None


def note_publish() -> None:
    LAST_PUBLISH.write_text(datetime.now(timezone.utc).isoformat(), encoding="utf-8")


def elapsed_text() -> str:
    last = _last_publish()
    if last is None:
        return "неизвестно (первая публикация)"
    minutes = (datetime.now(timezone.utc) - last).total_seconds() / 60
    if minutes < 90:
        return "%d мин" % round(minutes)
    return "%.1f ч" % (minutes / 60)


def publish_quota() -> int:
    """Сколько трансферов уместно выпустить в этом такте.

    Задумано было по одному раз в полчаса, но расписание GitHub этого не
    держит: оно объявлено «по возможности» и слоты роняет — за два часа
    приходило два прогона вместо пяти. Если публиковать строго по одному за
    такт, темп проседает вдвое-втрое и очередь растягивается на дни.

    Поэтому считаем не такты, а время: сколько получасовых окон прошло с
    прошлой публикации, столько и выпускаем. Средний темп остаётся прежним,
    просто пропущенное навёрстывается.

    Потолок нужен на случай долгого простоя: после суток тишины иначе
    вывалится полсотни страниц разом, а для поиска это выглядит свалкой —
    ровно то, чего мы избегали, когда выбирали штучную публикацию.
    """
    last = _last_publish()
    if last is None:
        return 1
    minutes = (datetime.now(timezone.utc) - last).total_seconds() / 60
    return max(1, min(MAX_PER_TICK, int(minutes // PACE_MINUTES)))


def enriched_count() -> int:
    if not RECORDS_DIR.exists():
        return 0
    total = 0
    for path in RECORDS_DIR.glob("*.json"):
        try:
            if json.loads(path.read_text(encoding="utf-8")).get(
                    "pipeline_state") == "ENRICHED":
                total += 1
        except Exception:
            continue
    return total


def next_job() -> Path | None:
    """Самый дорогой из неопубликованных: крупные сделки вперёд."""
    done = published()
    candidates = []
    for path in sorted(JOBS_DIR.glob("autopilot_*.json")):
        if path.name in done:
            continue
        try:
            job = json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            continue
        # Job — это снимок записи, и он переживает её. Запись могли снять
        # как негодную («Эвертон -> Эвертон»), а после публикации обогащение
        # само помечает её SKIPPED_DUPLICATE, увидев готовую страницу. В обоих
        # случаях файл job остаётся и каждый такт выбирается снова, роняя
        # публикацию. Условие простое: годен job, за которым стоит живая
        # обогащённая запись. Иначе снимаем.
        entity = (job.get("_autopilot") or {}).get("entity_id")
        if entity:
            record_path = RECORDS_DIR / ("%s.json" % entity)
            state = None
            if record_path.exists():
                try:
                    state = json.loads(
                        record_path.read_text(encoding="utf-8")).get("pipeline_state")
                except Exception:
                    state = None
            if state != "ENRICHED":
                print("  снят %s: запись %s — %s" % (
                    path.name, entity, state or "удалена"))
                path.unlink()
                continue
        points = (job.get("market_value_points") or
                  ((job.get("_autopilot") or {}).get("market_value_points")) or [])
        value = max([p.get("value_eur_m") or 0 for p in points] or [0])
        candidates.append((value, path))
    if not candidates:
        return None
    candidates.sort(key=lambda pair: -pair[0])
    return candidates[0][1]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Один такт автопилота")
    parser.add_argument("--no-discovery", action="store_true",
                        help="не читать ленты, работать только с очередью")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)
    ensure_dirs()

    print("=== ТАКТ АВТОПИЛОТА ===")

    if not args.no_discovery:
        print("\n[1] разведка")
        run("transfer_discovery.py", "--save")

    print("\n[2] обогащение")
    run("transfer_enrichment.py", "--all-kinds", "--save")

    ready = enriched_count()
    print("\n[3] сборка job (записей готово: %d)" % ready)
    if ready:
        run("job_builder.py", "--save")

    print("\n[4] публикация")
    quota = publish_quota()
    print("  с прошлой публикации прошло %s; норма на такт: %d"
          % (elapsed_text(), quota))

    published_now = 0
    code = 0
    while published_now < quota:
        job = next_job()
        if not job:
            print("  публиковать больше нечего")
            break

        print("\n  выбран: %s" % job.name)
        if args.dry_run:
            run("publisher.py", "--job", str(job), "--dry-run")
            return 0

        code = run("publisher.py", "--job", str(job))
        if code != 0:
            print("  публикация не прошла (код %d) — сайт откачен движком" % code)
            break

        remember(job.name)
        published_now += 1
        note_publish()

    if published_now:
        print("\n  опубликовано за такт: %d" % published_now)
        return 0
    if code == 0:
        print("\n  такт завершён без изменений")
    return code
    return code


if __name__ == "__main__":
    raise SystemExit(main())
