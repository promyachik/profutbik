"""
PROMYACHIK TRANSFER AUTOPILOT - PUBLISHER

Атомарная публикация одного трансфера замороженным движком 3.4.

Повторяет ровно ту последовательность, которая прошла серию 5/5 и четыре
ручных публикации, но без участия человека:

    targeted snapshot
    -> движок 3.4 (шаги 1-3)
    -> промоция в нижний тикер
    -> шаг 4: объект графика в PLAYERS
    -> бамп cache-token скрипта графика
    -> изолированный Hugo build
    -> rendered-валидация
    -> при любой ошибке после старта: ПОЛНЫЙ ОТКАТ

Движок не изменяется. Рендерер графика не изменяется: проверяется
отпечаток, и при его изменении публикация откатывается.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from transfer_discovery import ACTIVE_PROJECT, PARSER_ROOT  # noqa: E402

from paths import WORK as PROFUTBIK, ENGINE  # noqa: E402
PATCH_BACKUPS = PROFUTBIK / "patch-backups"
REPORTS = PROFUTBIK / "reports"
JOBS_DIR = PARSER_ROOT / "jobs"

TRANSFERS_JSON = ACTIVE_PROJECT / "data" / "transfers.json"
HOMEPAGE_JSON = ACTIVE_PROJECT / "data" / "homepage_transfer_rumor.json"
CLUB_LOGOS = ACTIVE_PROJECT / "data" / "club-logos.json"
CHART_JS = ACTIVE_PROJECT / "static" / "js" / "transfer-player-market-value-chart.js"
SINGLE_HTML = ACTIVE_PROJECT / "layouts" / "transfers" / "single.html"

SNAPSHOT_FILES = [TRANSFERS_JSON, HOMEPAGE_JSON, CLUB_LOGOS, CHART_JS, SINGLE_HTML]

MONTHS_SHORT = ["янв.", "февр.", "март", "апр.", "май", "июнь",
                "июль", "авг.", "сент.", "окт.", "нояб.", "дек."]


class PublishError(Exception):
    """Ошибка после старта транзакции. Требует полного отката."""


def now_stamp() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def log(message: str) -> None:
    print("  %s" % message, flush=True)


# ---------------------------------------------------------------------------
# Транзакция
# ---------------------------------------------------------------------------

class Transaction:
    def __init__(self, slug: str):
        self.slug = slug
        self.root = PATCH_BACKUPS / ("%s_AUTOPILOT_%s_PRE" % (now_stamp(), slug.upper()))
        self.created_paths: list[Path] = []
        self.started = False

    def snapshot(self) -> None:
        self.root.mkdir(parents=True, exist_ok=True)
        for path in SNAPSHOT_FILES:
            if not path.exists():
                continue
            destination = self.root / path.relative_to(ACTIVE_PROJECT)
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, destination)
        self.started = True
        log("snapshot: %s" % self.root)

    def track_created(self, path: Path) -> None:
        self.created_paths.append(path)

    def rollback(self) -> list[str]:
        restored: list[str] = []
        for path in SNAPSHOT_FILES:
            backup = self.root / path.relative_to(ACTIVE_PROJECT)
            if backup.exists():
                shutil.copy2(backup, path)
                restored.append(str(path))
        for path in self.created_paths:
            if path.is_dir():
                shutil.rmtree(path, ignore_errors=True)
                restored.append("removed dir %s" % path)
            elif path.exists():
                path.unlink()
                restored.append("removed %s" % path)
        return restored


# ---------------------------------------------------------------------------
# Шаги публикации
# ---------------------------------------------------------------------------

def run_engine(job_path: Path) -> None:
    result = subprocess.run(
        [sys.executable, str(ENGINE), str(job_path),
         "--active-project", str(ACTIVE_PROJECT)],
        capture_output=True, text=True, encoding="utf-8", errors="replace",
        timeout=900)
    if result.returncode != 0:
        tail = (result.stdout or "")[-6000:] + (result.stderr or "")[-6000:]
        raise PublishError("движок вернул код %d: %s" % (result.returncode, tail))
    if "transfer_news_4_step_pipeline_applied" not in (result.stdout or ""):
        raise PublishError("движок не подтвердил применение изменений")


def promote_lower_ticker(slug: str) -> None:
    data = json.loads(TRANSFERS_JSON.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise PublishError("transfers.json не список")
    targets = [row for row in data if row.get("slug") == slug]
    if len(targets) != 1:
        raise PublishError("записей target = %d, ожидалась одна" % len(targets))
    target = targets[0]
    if target.get("show_in_footer_ticker") is not True:
        raise PublishError("у target не выставлен show_in_footer_ticker")
    rest = [row for row in data if row.get("slug") != slug]
    TRANSFERS_JSON.write_text(
        json.dumps([target] + rest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8")


def players_span(text: str):
    match = re.search(r"const\s+PLAYERS\s*=\s*", text)
    if not match:
        raise PublishError("const PLAYERS не найден в скрипте графика")
    start = match.end()
    while text[start].isspace():
        start += 1
    array, length = json.JSONDecoder().raw_decode(text[start:])
    return start, start + length, array


def renderer_fingerprint(text: str) -> str:
    start, end, _ = players_span(text)
    return hashlib.sha256(
        (text[:start] + "__PLAYERS_DATA__" + text[end:]).encode("utf-8")).hexdigest()


def short_date(iso: str) -> str:
    try:
        parsed = datetime.strptime(iso[:10], "%Y-%m-%d")
    except Exception:
        return iso[:10]
    return "%s %d" % (MONTHS_SHORT[parsed.month - 1], parsed.year)


def club_asset(api_id: int, fallback_name: str) -> tuple[str, str]:
    """(путь логотипа, короткий код клуба) из каталога, обновлённого движком.

    Каталог ведёт сам движок, поэтому читаем его ПОСЛЕ запуска движка:
    к этому моменту там уже актуальный versioned-путь.
    """
    catalog = json.loads(CLUB_LOGOS.read_text(encoding="utf-8"))
    clubs = catalog.get("clubs", catalog)
    entry = (clubs or {}).get(str(api_id)) or {}
    code = (entry.get("code") or fallback_name[:3]).upper()

    logo = ""
    for key in ("logo", "published_path", "path", "rendered"):
        value = entry.get(key)
        if value and str(value).endswith(".png"):
            logo = str(value).lstrip("/")
            break
    if not logo:
        raise PublishError("не найден логотип клуба API %s в club-logos.json" % api_id)
    if not (ACTIVE_PROJECT / "static" / Path(logo)).exists():
        raise PublishError("файл логотипа отсутствует: %s" % logo)
    return logo, code


def full_history_points(job: dict) -> list[dict] | None:
    """PF527A — настоящий путь игрока вместо двух клубов.

    Раньше точки графика собирались так: все, кроме последней, приписывались
    клубу «откуда», последняя — клубу «куда». То есть путь у любого игрока
    состоял ровно из двух клубов, даже если он сменил пять. Дмитрий это и
    заметил: у Аханора на графике «Аталанта → Кристал Пэлас», а «Дженоа», где
    он играл между ними, нет вовсе.

    Причина глубже отрисовки. Обогащение брало у Transfermarkt только три
    поля — пик, предыдущую и текущую оценку, — и в записи оказывалось две-три
    точки. Полная история лежит по другому адресу и содержит клуб на каждой
    дате: у того же Аханора там семь точек.

    Здесь берём именно её и отдаём каждой точке её собственный клуб. Всю
    работу делает market_value_chart — он умеет и отбирать значимые точки, и
    доставать эмблемы клубов вне наших восьми лиг с CDN Transfermarkt.

    Если сеть подвела — возвращаем None, и публикация идёт по прежнему пути.
    График с двумя клубами хуже полного, но лучше сорванной публикации.
    """
    player_id = job.get("transfermarkt_player_id")
    if not player_id:
        return None
    try:
        import market_value_chart as mvc

        history = mvc.market_history(str(player_id))
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
            if club_id not in clubs:
                clubs[club_id] = mvc.resolve_club(club_id, history, index)
            points.append({"label": label, "value_label": value_label,
                           "value": round(row["value"] / 1_000_000, 2),
                           "club": clubs[club_id]})
        return points if len(points) >= 2 else None
    except Exception as error:  # noqa: BLE001
        log("полная история не получена (%s) — график по двум клубам"
            % str(error)[:120])
        return None


def inject_graph(job: dict, points: list[dict]) -> None:
    if not points:
        raise PublishError("нет точек рыночной стоимости для графика")

    text = CHART_JS.read_text(encoding="utf-8")
    before = renderer_fingerprint(text)
    start, end, array = players_span(text)

    slug = job["slug"]
    key = "%s-step4" % slug

    built = full_history_points(job)
    if built:
        clubs_seen = len({point["club"]["name"] for point in built})
        log("график: точек %d, клубов в пути %d" % (len(built), clubs_seen))
        array = [p for p in array if p.get("key") != key]
        array.append({"key": key, "name": job["player"],
                      "paths": ["/transfers/%s/" % slug], "points": built})
        updated = text[:start] + json.dumps(array, ensure_ascii=False) + text[end:]
        if renderer_fingerprint(updated) != before:
            raise PublishError("отпечаток рендерера графика изменился")
        CHART_JS.write_text(updated, encoding="utf-8", newline="")
        return
    from_logo, from_code = club_asset(job["from_club_id"], job["from_club_name"])
    to_logo, to_code = club_asset(job["to_club_id"], job["to_club_name"])
    from_club = {
        "slug": re.sub(r"[^a-z0-9]+", "-", job["from_club_name"].lower()).strip("-"),
        "name": job["from_club_name"], "short": from_code,
        "api_id": job["from_club_id"], "period": "до %s" % short_date(points[-1]["date"]),
        "logo": from_logo,
    }
    to_club = {
        "slug": re.sub(r"[^a-z0-9]+", "-", job["to_club_name"].lower()).strip("-"),
        "name": job["to_club_name"], "short": to_code,
        "api_id": job["to_club_id"], "period": "с %s" % short_date(points[-1]["date"]),
        "logo": to_logo,
    }

    built = []
    for index, point in enumerate(points):
        club = to_club if index == len(points) - 1 else from_club
        value = point["value_eur_m"]
        built.append({
            "label": short_date(point["date"]),
            "value_label": "€%s млн" % ("%g" % value).replace(".", ","),
            "value": float(value),
            "club": dict(club),
        })

    array = [p for p in array if p.get("key") != key]
    array.append({"key": key, "name": job["player"],
                  "paths": ["/transfers/%s/" % slug], "points": built})

    updated = text[:start] + json.dumps(array, ensure_ascii=False) + text[end:]
    if renderer_fingerprint(updated) != before:
        raise PublishError("отпечаток рендерера графика изменился")
    CHART_JS.write_text(updated, encoding="utf-8", newline="")


def bump_cache_token() -> str:
    """Без бампа браузер отдаёт старый скрипт, и график у нового игрока не появится."""
    # Точность до секунды: две публикации в одну минуту получали одинаковый
    # токен, и у второго игрока график мог не появиться из-за кэша браузера.
    token = "ap%s" % datetime.now().strftime("%m%d%H%M%S")
    text = SINGLE_HTML.read_text(encoding="utf-8")
    pattern = r"(transfer-player-market-value-chart\.js)(?:\?v=[^\"\s<}]+)?"
    updated, count = re.subn(pattern, r"\1?v=" + token, text, count=1)
    if count != 1:
        raise PublishError("ссылка на скрипт графика не найдена в single.html")
    SINGLE_HTML.write_text(updated, encoding="utf-8", newline="")
    return token


def hugo_build() -> Path:
    destination = Path(tempfile.mkdtemp(prefix="promyachik_build_"))
    result = subprocess.run(
        ["hugo", "--destination", str(destination), "--cleanDestinationDir",
         "--logLevel", "error"],
        cwd=str(ACTIVE_PROJECT), capture_output=True, text=True,
        encoding="utf-8", errors="replace", timeout=600)
    if result.returncode != 0:
        shutil.rmtree(destination, ignore_errors=True)
        raise PublishError("Hugo build упал: %s" % (result.stderr or "")[-500:])
    return destination


def strip_lower_ticker(html: str) -> str:
    marker = "bottom-transfer-strip-v3 home-player-bottom-strip"
    index = html.find(marker)
    if index < 0:
        return ""
    start = html.rfind("<section", 0, index)
    end = html.find("</section>", index)
    return html[start: end + 10 if end > 0 else index + 160000]


def validate(build: Path, job: dict, token: str) -> list[str]:
    slug = job["slug"]
    player = job["player"]
    checks: list[str] = []

    def require(condition: bool, label: str) -> None:
        checks.append("%s %s" % ("PASS" if condition else "FAIL", label))
        if not condition:
            raise PublishError("rendered-проверка не прошла: %s" % label)

    page_path = build / "transfers" / slug / "index.html"
    require(page_path.exists(), "страница трансфера создана")
    page = page_path.read_text(encoding="utf-8", errors="replace")
    home = (build / "index.html").read_text(encoding="utf-8", errors="replace")

    require(player in home, "ШАГ 1: игрок на главной")
    require("transfers/%s/" % slug in home, "ШАГ 1: ссылка с главной")
    require(home.count(player) >= 2, "ШАГ 2: верхний тикер")
    require(player in page, "ШАГ 3: имя на странице")
    image = "%s-%s-black.png" % (slug, job["transfermarkt_player_id"])
    require(image in page, "ШАГ 3: портрет подключён")
    require((build / "images" / "players" / "transfermarkt" / image).exists(),
            "ШАГ 3: файл портрета в сборке")

    script = (build / "js" / "transfer-player-market-value-chart.js").read_text(
        encoding="utf-8", errors="replace")
    _, _, array = players_span(script)
    objects = [p for p in array if p.get("key") == "%s-step4" % slug]
    require(len(objects) == 1, "ШАГ 4: ровно один объект графика")
    for point in objects[0]["points"]:
        logo = point["club"]["logo"]
        require((build / Path(logo)).exists(), "ШАГ 4: логотип %s" % point["club"]["short"])
    require("chart.js?v=%s" % token in page, "ШАГ 4: свежий cache-token")

    require(bool(strip_lower_ticker(home)), "нижний тикер: маркер на главной")
    require(player.split()[-1] in strip_lower_ticker(home),
            "нижний тикер: игрок на главной")
    require(player.split()[-1] in strip_lower_ticker(page),
            "нижний тикер: игрок на странице")
    require("pf407z-transfer-single-ticker-fullbleed" in page,
            "full-bleed 407Z на месте")
    return checks


# ---------------------------------------------------------------------------

def promote_from_rumor(slug: str, job: dict) -> list[str]:
    """Если по этому же игроку был опубликован слух - снять его и не потерять адрес.

    Слух и трансфер живут по разным адресам, поэтому при повышении старый
    адрес умер бы. Прописываем aliases в front matter трансфера: Hugo сам
    сгенерирует редирект, и накопленные ссылки не пропадут.
    """
    entity_id = (job.get("_autopilot") or {}).get("entity_id") or ""
    rumor_slug = ""
    rumors_dir = ACTIVE_PROJECT / "content" / "rumors"
    if rumors_dir.exists():
        for directory in rumors_dir.iterdir():
            page = directory / "index.md"
            if not page.is_file():
                continue
            head = page.read_text(encoding="utf-8", errors="replace")[:1500]
            if entity_id and entity_id in head:
                rumor_slug = directory.name
                break
    if not rumor_slug:
        return []

    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from rumor_publisher import remove_rumor

    done = remove_rumor(rumor_slug)

    target = ACTIVE_PROJECT / "content" / "transfers" / slug / "index.md"
    if target.exists():
        text = target.read_text(encoding="utf-8")
        alias = "/rumors/%s/" % rumor_slug
        if "aliases:" not in text and text.startswith("---"):
            end = text.find("\n---", 3)
            if end > 0:
                text = text[:end] + '\naliases: ["%s"]' % alias + text[end:]
                target.write_text(text, encoding="utf-8")
                done.append("редирект с %s" % alias)
    return done


def publish(job_path: Path, dry_run: bool = False) -> dict:
    job = json.loads(job_path.read_text(encoding="utf-8"))
    slug = job["slug"]
    points = (job.get("_autopilot") or {}).get("market_value_points") or []

    print("\n=== ПУБЛИКАЦИЯ: %s ===" % slug)
    if dry_run:
        log("DRY RUN: сайт не изменяется")
        return {"slug": slug, "site_changed": False, "dry_run": True}

    transaction = Transaction(slug)
    page_dir = ACTIVE_PROJECT / "content" / "transfers" / slug
    image_path = (ACTIVE_PROJECT / "static" / "images" / "players" / "transfermarkt"
                  / ("%s-%s-black.png" % (slug, job["transfermarkt_player_id"])))
    build_dir: Path | None = None

    try:
        transaction.snapshot()
        if not page_dir.exists():
            transaction.track_created(page_dir)
        if not image_path.exists():
            transaction.track_created(image_path)

        log("движок 3.4: шаги 1-3")
        run_engine(job_path)

        log("промоция в нижний тикер")
        promote_lower_ticker(slug)

        log("шаг 4: объект графика")
        inject_graph(job, points)

        token = bump_cache_token()
        log("cache-token: %s" % token)

        log("изолированный Hugo build")
        build_dir = hugo_build()

        log("rendered-валидация")
        checks = validate(build_dir, job, token)
        for line in checks:
            log("   " + line)

        promoted = promote_from_rumor(slug, job)
        for line in promoted:
            log("повышение из слуха: %s" % line)

        log("ОПУБЛИКОВАНО")
        return {"slug": slug, "site_changed": True, "rolled_back": False,
                "checks": checks, "token": token, "promoted_from_rumor": promoted,
                "snapshot": str(transaction.root)}

    except Exception as error:
        restored = transaction.rollback() if transaction.started else []
        # Обрезка на 200 символах экономила место в консоли и стоила разбора:
        # причина отказа движка всегда в хвосте его вывода, а именно он и
        # отрезался. В облаке лог читать больше неоткуда — печатаем целиком.
        for line in str(error).replace("\\n", "\n").split("\n"):
            log("ОШИБКА: %s" % line)
        log("ОТКАТ ВЫПОЛНЕН, восстановлено объектов: %d" % len(restored))
        return {"slug": slug, "site_changed": False, "rolled_back": True,
                "error": str(error), "restored": restored,
                "snapshot": str(transaction.root)}
    finally:
        if build_dir:
            shutil.rmtree(build_dir, ignore_errors=True)


# ---------------------------------------------------------------------------
# Снятие трансфера с сайта
# ---------------------------------------------------------------------------

def unpublish(slug: str) -> dict:
    """Полностью убирает трансфер с сайта.

    Симметрично публикации: страница, запись в данных, запись на главной,
    объект графика и портрет. Перед изменением делается снимок, чтобы
    операцию можно было отменить.
    """
    transaction = Transaction("unpublish-%s" % slug)
    removed: list[str] = []
    try:
        transaction.snapshot()

        data = json.loads(TRANSFERS_JSON.read_text(encoding="utf-8"))
        kept = [row for row in data if row.get("slug") != slug]
        if len(kept) != len(data):
            TRANSFERS_JSON.write_text(
                json.dumps(kept, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8")
            removed.append("transfers.json: -%d" % (len(data) - len(kept)))

        homepage = json.loads(HOMEPAGE_JSON.read_text(encoding="utf-8"))
        for section in ("transfers", "rumors"):
            rows = homepage.get(section) or []
            left = [row for row in rows if row.get("slug") != slug]
            if len(left) != len(rows):
                homepage[section] = left
                removed.append("homepage/%s: -%d" % (section, len(rows) - len(left)))
        HOMEPAGE_JSON.write_text(
            json.dumps(homepage, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8")

        text = CHART_JS.read_text(encoding="utf-8")
        before = renderer_fingerprint(text)
        start, end, array = players_span(text)
        left = [p for p in array if p.get("key") != "%s-step4" % slug]
        if len(left) != len(array):
            updated = text[:start] + json.dumps(left, ensure_ascii=False) + text[end:]
            if renderer_fingerprint(updated) != before:
                raise PublishError("отпечаток рендерера изменился при удалении")
            CHART_JS.write_text(updated, encoding="utf-8", newline="")
            removed.append("график: объект удалён")

        page_dir = ACTIVE_PROJECT / "content" / "transfers" / slug
        if page_dir.exists():
            shutil.rmtree(page_dir)
            removed.append("страница удалена")

        images = ACTIVE_PROJECT / "static" / "images" / "players" / "transfermarkt"
        for image in images.glob("%s-*-black.png" % slug):
            image.unlink()
            removed.append("портрет удалён")

        bump_cache_token()
        build_dir = hugo_build()
        home = (build_dir / "index.html").read_text(encoding="utf-8", errors="replace")
        shutil.rmtree(build_dir, ignore_errors=True)
        if "transfers/%s/" % slug in home:
            raise PublishError("ссылка на трансфер осталась на главной после удаления")

        return {"slug": slug, "unpublished": True, "removed": removed,
                "snapshot": str(transaction.root)}
    except Exception as error:
        transaction.rollback()
        return {"slug": slug, "unpublished": False, "error": str(error),
                "snapshot": str(transaction.root)}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Promyachik autopilot publisher")
    parser.add_argument("--job", help="конкретный job.json")
    parser.add_argument("--all", action="store_true", help="все job из parser/jobs")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--unpublish", help="убрать трансфер с сайта по slug")
    args = parser.parse_args(argv)

    if args.unpublish:
        result = unpublish(args.unpublish)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0 if result.get("unpublished") else 1

    if args.job:
        jobs = [Path(args.job)]
    elif args.all:
        jobs = sorted(JOBS_DIR.glob("autopilot_*.json"))
    else:
        parser.error("нужен --job, --all или --unpublish")

    results = [publish(path, dry_run=args.dry_run) for path in jobs]

    REPORTS.mkdir(parents=True, exist_ok=True)
    report = REPORTS / ("%s_AUTOPILOT_PUBLISH.json" % now_stamp())
    report.write_text(json.dumps(results, ensure_ascii=False, indent=2),
                      encoding="utf-8")

    published = sum(1 for r in results if r.get("site_changed"))
    rolled = sum(1 for r in results if r.get("rolled_back"))
    print("\n=== ИТОГ: опубликовано %d, откачено %d ===" % (published, rolled))
    print("отчёт: %s\n" % report)
    return 0 if rolled == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
