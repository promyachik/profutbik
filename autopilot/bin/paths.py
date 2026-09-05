"""
PROMYACHIK — КОРНИ ПРОЕКТА В ОДНОМ МЕСТЕ

Пути раньше были прибиты в пяти модулях по отдельности. Пока всё крутилось
на машине Дмитрия, это работало; для запуска в GitHub Actions — нет.

Значения берутся из переменных окружения, а если их нет — остаются прежние
локальные. То есть локальный запуск ведёт себя ровно как раньше, а в облаке
корни задаются окружением.

Правило проекта соблюдено: путь по-прежнему **явный**. Запрещённого
`Path(__file__).resolve().parents[1]` здесь нет — оно указывало бы на runner,
и правки уходили бы не в тот проект.

    PROMYACHIK_SITE    корень активного сайта (Promyachik_CLEAN)
    PROMYACHIK_PARSER  корень парсера (state, jobs, config)
    PROMYACHIK_ENGINE  файл замороженного движка 3.4
    PROMYACHIK_WORK    отчёты, снимки для отката, временные файлы
"""
from __future__ import annotations

import os
from pathlib import Path


def _root(env: str, default: str) -> Path:
    return Path(os.environ.get(env) or default)


SITE = _root("PROMYACHIK_SITE", r"C:\Users\Dmitrii\Promyachik_CLEAN")
PARSER_ROOT = _root("PROMYACHIK_PARSER", r"C:\Users\Dmitrii\ProFutbik\parser")
WORK = _root("PROMYACHIK_WORK", r"C:\Users\Dmitrii\ProFutbik")
ENGINE = _root(
    "PROMYACHIK_ENGINE",
    r"C:\Users\Dmitrii\Promyachik\01_CANONICAL_485A\transfer-news-4-step-pipeline.py",
)

RECORDS_DIR = PARSER_ROOT / "state" / "records"
HISTORY_DIR = PARSER_ROOT / "state" / "history"
CACHE_DIR = PARSER_ROOT / "state" / "cache"
JOBS_DIR = PARSER_ROOT / "jobs"
QUEUES_DIR = PARSER_ROOT / "queues"
RAW_DIR = PARSER_ROOT / "raw"

REPORTS = WORK / "reports"
BACKUPS = WORK / "patch-backups"
TEMP = WORK / "temp"

# Ключ API-Football. В облаке приходит переменной окружения и в файлах
# не хранится вовсе — репозиторий публичный.
ENV_FILES = [
    Path(os.environ.get("PROMYACHIK_ENV_FILE") or r"C:\Users\Dmitrii\Promyachik\.env"),
    WORK / "config" / "api-football.env",
]


def ensure_dirs() -> None:
    """В облаке рабочих папок может не быть — создаём молча."""
    for path in (RECORDS_DIR, HISTORY_DIR, CACHE_DIR, JOBS_DIR,
                 QUEUES_DIR, RAW_DIR, REPORTS, BACKUPS, TEMP):
        path.mkdir(parents=True, exist_ok=True)


def describe() -> str:
    return "\n".join([
        "  сайт:    %s" % SITE,
        "  парсер:  %s" % PARSER_ROOT,
        "  движок:  %s" % ENGINE,
        "  рабочая: %s" % WORK,
    ])


if __name__ == "__main__":
    print("Корни проекта:")
    print(describe())
    print("\nПроверка наличия:")
    for label, path in (("сайт", SITE), ("парсер", PARSER_ROOT),
                        ("движок", ENGINE), ("рабочая", WORK)):
        print("  %-9s %s  %s" % (label, "есть " if path.exists() else "НЕТ  ", path))
