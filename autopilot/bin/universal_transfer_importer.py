# -*- coding: utf-8 -*-
from __future__ import annotations

from datetime import datetime
from pathlib import Path
import argparse
import hashlib
import json
import re
import shutil
import subprocess
import traceback
import unicodedata

PROJECTS = [
    Path(r"C:\Users\Dmitrii\Promyachik_CLEAN"),
    Path(r"C:\Users\Dmitrii\Promyachik"),
]

REPORT_DEFAULT = Path(
    r"C:\Users\Dmitrii\ProFutbik\reports"
    r"\UNIVERSAL_TRANSFER_IMPORTER_LATEST.txt"
)
BACKUPS = Path(r"C:\Users\Dmitrii\ProFutbik\patch-backups")
TEMP_ROOT = Path(r"C:\Users\Dmitrii\ProFutbik\temp")

HOME_DATA_REL = Path("data/homepage_transfer_rumor.json")
TICKER_DATA_REL = Path("data/transfers.json")
UPPER_PARTIAL_REL = Path("layouts/partials/transfer-ticker.html")
LOWER_PARTIAL_REL = Path("layouts/partials/home-player-bottom-strip.html")

LOG = []
REPORT = REPORT_DEFAULT


def log(message=""):
    text = str(message)
    print(text, flush=True)
    LOG.append(text)
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text("\n".join(LOG) + "\n", encoding="utf-8")


def detect_project():
    for root in PROJECTS:
        if (root / "hugo.toml").exists():
            return root
    raise FileNotFoundError("hugo.toml not found")


def find_hugo():
    for candidate in (
        Path(r"C:\Hugo\hugo.exe"),
        Path(r"C:\Program Files\Hugo\hugo.exe"),
    ):
        if candidate.exists():
            return str(candidate)
    result = subprocess.run(
        ["where", "hugo"],
        capture_output=True,
        text=True,
        errors="replace",
        shell=True,
    )
    for line in (result.stdout or "").splitlines():
        if line.strip():
            return line.strip()
    raise FileNotFoundError("hugo.exe not found")


def read(path):
    return path.read_text(encoding="utf-8-sig", errors="replace")


def load_json(path):
    return json.loads(read(path))


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_text(
        json.dumps(value, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    temp.replace(path)


def slugify(value):
    normalized = unicodedata.normalize("NFKD", value)
    ascii_value = normalized.encode("ascii", "ignore").decode("ascii")
    result = re.sub(r"[^a-z0-9]+", "-", ascii_value.lower()).strip("-")
    if not result:
        raise ValueError("Unable to create slug")
    return result


def yaml_string(value):
    value = str(value or "").replace("\\", "\\\\").replace('"', '\\"')
    return f'"{value}"'


def parse_date(value):
    return datetime.fromisoformat(str(value).strip().replace("Z", "+00:00"))


def stable_player_id(entity_id):
    digest = hashlib.sha256(entity_id.encode("utf-8")).hexdigest()
    return int(digest[:8], 16)


def validate_input(data):
    for key in (
        "entity_id",
        "player",
        "from_club",
        "to_club",
        "date",
        "status",
    ):
        if key not in data:
            raise ValueError(f"Missing input field: {key}")

    for side in ("from_club", "to_club"):
        if not isinstance(data[side], dict):
            raise TypeError(f"{side} must be an object")
        for key in ("id", "name", "logo"):
            if key not in data[side]:
                raise ValueError(f"Missing input field: {side}.{key}")

    if not re.search(r"[A-Za-z]", str(data["player"])):
        raise ValueError("player must use Latin spelling")

    if str(data["status"]).lower() not in {"official", "completed"}:
        raise ValueError(
            "Stage 1 accepts only official/completed transfers"
        )

    if data.get("outputs", {}).get("lower_ticker") is True:
        raise ValueError(
            "Lower ticker is disabled during stage 1 testing"
        )


def canonical_slug(data):
    explicit = str(data.get("slug") or "").strip()
    if explicit:
        return explicit
    return slugify(f"{data['player']} {data['to_club']['name']}")


def item_club_name(item, side):
    nested = item.get(f"{side}_club")
    if isinstance(nested, dict):
        return str(nested.get("name") or "").strip().lower()
    return str(
        item.get(f"{side}_name")
        or item.get(f"{side}_club_name")
        or ""
    ).strip().lower()


def entity_matches(item, data, slug, url):
    if not isinstance(item, dict):
        return False

    if str(item.get("entity_id") or "") == str(data["entity_id"]):
        return True
    if str(item.get("slug") or "") == slug:
        return True
    if str(item.get("url") or "").lstrip("/") == url.lstrip("/"):
        return True

    return (
        str(item.get("player") or "").strip().lower()
        == str(data["player"]).strip().lower()
        and item_club_name(item, "from")
        == str(data["from_club"]["name"]).strip().lower()
        and item_club_name(item, "to")
        == str(data["to_club"]["name"]).strip().lower()
    )


def fee_display(data):
    return str(
        data.get("fee_display")
        or data.get("fee")
        or "Сумма не раскрыта"
    )


def build_page(data, slug, page_url):
    player = str(data["player"])
    from_name = str(data["from_club"]["name"])
    to_name = str(data["to_club"]["name"])
    fee = fee_display(data)
    title = str(
        data.get("title_ru")
        or f"{player} перешёл из {from_name} в {to_name}"
    )
    intro = str(
        data.get("intro_ru")
        or f"{to_name} официально объявил о переходе "
           f"{player} из {from_name}."
    )
    description = str(data.get("seo_description") or intro)
    player_id = int(
        data.get("player_id")
        or stable_player_id(str(data["entity_id"]))
    )

    return "\n".join([
        "---",
        f"title: {yaml_string(title)}",
        f"date: {yaml_string(data['date'])}",
        "draft: true",
        'type: "transfers"',
        'layout: "single"',
        f"slug: {yaml_string(slug)}",
        f"url: {yaml_string('/' + page_url)}",
        f"description: {yaml_string(description)}",
        f"summary: {yaml_string(intro)}",
        f"entity_id: {yaml_string(data['entity_id'])}",
        f"player: {yaml_string(player)}",
        f"player_name: {yaml_string(player)}",
        f"player_id: {player_id}",
        f"from_club: {yaml_string(from_name)}",
        f"from_name: {yaml_string(from_name)}",
        f"from_club_name: {yaml_string(from_name)}",
        f"from_club_id: {int(data['from_club']['id'])}",
        f"from_club_logo: {yaml_string(data['from_club']['logo'])}",
        f"to_club: {yaml_string(to_name)}",
        f"to_name: {yaml_string(to_name)}",
        f"to_club_name: {yaml_string(to_name)}",
        f"to_club_id: {int(data['to_club']['id'])}",
        f"to_club_logo: {yaml_string(data['to_club']['logo'])}",
        f"fee: {yaml_string(fee)}",
        f"amount: {yaml_string(fee)}",
        f"transfer_fee: {yaml_string(fee)}",
        'status: "completed"',
        'canonical_transfer_status: "official"',
        'status_label: "СОСТОЯЛСЯ"',
        f"league: {yaml_string(data.get('league', ''))}",
        f"source_url: {yaml_string(data.get('source_url', ''))}",
        "show_in_top_ticker: true",
        "show_in_footer_ticker: false",
        f"test_mode: {'true' if data.get('test_mode', True) else 'false'}",
        "parser_generated: true",
        "---",
        "",
        intro,
        "",
        "## Данные трансфера",
        "",
        f"- Игрок: **{player}**",
        f"- Из клуба: **{from_name}**",
        f"- В клуб: **{to_name}**",
        f"- Сумма: **{fee}**",
        "- Статус: **СОСТОЯЛСЯ**",
        "",
    ])


def build_home_item(data, slug, page_url):
    from_club = data["from_club"]
    to_club = data["to_club"]
    player = str(data["player"])
    title = str(
        data.get("title_ru")
        or f"{player} перешёл из {from_club['name']} "
           f"в {to_club['name']}"
    )

    return {
        "entity_id": data["entity_id"],
        "date": data["date"],
        "fee": fee_display(data),
        "from_club_id": str(from_club["id"]),
        "from_club_name_en": from_club["name"],
        "from_logo": from_club["logo"],
        "from_name": from_club["name"],
        "group": "transfer",
        "parser_generated": True,
        "player": player,
        "player_name_en": player,
        "slug": slug,
        "sort_ts": parse_date(data["date"]).timestamp(),
        "status": "completed",
        "status_css": "is-done",
        "status_display": "состоялся",
        "test_mode": bool(data.get("test_mode", True)),
        "title": title,
        "to_club_id": str(to_club["id"]),
        "to_club_name_en": to_club["name"],
        "to_logo": to_club["logo"],
        "to_name": to_club["name"],
        "url": page_url,
    }


def build_ticker_item(data, slug, page_url):
    entity_id = str(data["entity_id"])
    from_club = data["from_club"]
    to_club = data["to_club"]
    player_id = int(
        data.get("player_id") or stable_player_id(entity_id)
    )

    from_object = {
        "id": int(from_club["id"]),
        "name": str(from_club["name"]),
        "configured_name": str(from_club["name"]),
        "logo": str(from_club["logo"]),
    }
    to_object = {
        "id": int(to_club["id"]),
        "name": str(to_club["name"]),
        "configured_name": str(to_club["name"]),
        "logo": str(to_club["logo"]),
    }

    return {
        "entity_id": entity_id,
        "cutout_player_image": "",
        "date": data["date"],
        "fee": fee_display(data),
        "from_club": from_object,
        "from_club_id": int(from_club["id"]),
        "from_club_logo": str(from_club["logo"]),
        "from_club_name": str(from_club["name"]),
        "parser_generated": True,
        "player": str(data["player"]),
        "player_id": player_id,
        "player_image": "",
        "player_image_background_removed": False,
        "player_image_fallback": "",
        "player_image_processor": "pending",
        "show_in_footer_ticker": False,
        "show_in_top_ticker": True,
        "slug": slug,
        "status": "completed",
        "status_label": "СОСТОЯЛСЯ",
        "test_mode": bool(data.get("test_mode", True)),
        "ticker_image": "",
        "to_club": to_object,
        "to_club_id": int(to_club["id"]),
        "to_club_logo": str(to_club["logo"]),
        "to_club_name": str(to_club["name"]),
        "url": page_url,
    }


def backup_path(root, path, backup_root):
    if not path.exists():
        return None
    destination = backup_root / path.relative_to(root)
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(path, destination)
    return destination


def restore_path(path, backup):
    if backup is None:
        path.unlink(missing_ok=True)
    else:
        path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(backup, path)


def build_site(root, hugo, temp):
    shutil.rmtree(temp, ignore_errors=True)
    temp.mkdir(parents=True, exist_ok=True)
    result = subprocess.run(
        [hugo, "-D", "--minify", "--destination", str(temp)],
        cwd=str(root),
        capture_output=True,
        text=True,
        errors="replace",
    )
    log(f"HUGO_EXIT_CODE: {result.returncode}")
    if result.returncode != 0:
        raise RuntimeError(
            result.stderr or result.stdout or "Hugo build failed"
        )


def locate_home(temp):
    preferred = temp / "index.html"
    if preferred.exists():
        html = read(preferred)
        if "pf-home-panel--transfers" in html:
            return preferred, html

    for path in temp.rglob("index.html"):
        html = read(path)
        if (
            "pf-home-panel--transfers" in html
            and "pf-ticker__item" in html
        ):
            return path, html
    raise RuntimeError("Rendered homepage not found")


def locate_transfer(temp, slug):
    for path in temp.rglob("index.html"):
        if slug in path.as_posix():
            return path, read(path)
    raise RuntimeError("Rendered transfer page not found")


def ordered_context_contains(html, marker, player, slug):
    search_from = 0
    while True:
        position = html.lower().find(marker.lower(), search_from)
        if position < 0:
            return False

        block = html[position:min(len(html), position + 50000)]
        if player.lower() in block.lower() and slug.lower() in block.lower():
            return True

        search_from = position + len(marker)


def main(input_path, report_path):
    global REPORT
    REPORT = report_path
    data = load_json(input_path)
    validate_input(data)

    log("STEP: UNIVERSAL_TRANSFER_IMPORTER")
    log("STARTED_AT: " + datetime.now().isoformat(timespec="seconds"))
    log(f"INPUT_FILE: {input_path}")
    log(f"ENTITY_ID: {data['entity_id']}")
    log(f"PLAYER: {data['player']}")
    log("PLAYER_SPECIFIC_CODE: False")
    log("PUBLIC_GITHUB_PUBLISH: False")
    log("LOWER_TICKER_STAGE: disabled")

    root = detect_project()
    hugo = find_hugo()
    slug = canonical_slug(data)
    page_url = f"transfers/{slug}/"

    content_path = root / "content" / "transfers" / slug / "index.md"
    home_data_path = root / HOME_DATA_REL
    ticker_data_path = root / TICKER_DATA_REL
    upper_partial = root / UPPER_PARTIAL_REL
    lower_partial = root / LOWER_PARTIAL_REL

    for path in (
        home_data_path,
        ticker_data_path,
        upper_partial,
        lower_partial,
    ):
        if not path.exists():
            raise FileNotFoundError(path)

    upper_hash = hashlib.sha256(upper_partial.read_bytes()).hexdigest()
    lower_hash = hashlib.sha256(lower_partial.read_bytes()).hexdigest()

    stamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    backup_root = BACKUPS / f"UNIVERSAL_IMPORT_{stamp}_{slug}"
    backups = {
        content_path: backup_path(root, content_path, backup_root),
        home_data_path: backup_path(root, home_data_path, backup_root),
        ticker_data_path: backup_path(root, ticker_data_path, backup_root),
    }
    log(f"TARGETED_BACKUP: {backup_root}")

    content_path.parent.mkdir(parents=True, exist_ok=True)
    content_path.write_text(
        build_page(data, slug, page_url),
        encoding="utf-8",
    )

    home_data = load_json(home_data_path)
    if not isinstance(home_data.get("transfers"), list):
        raise TypeError("homepage transfers must be an array")

    home_items = [
        item
        for item in home_data["transfers"]
        if not entity_matches(item, data, slug, page_url)
    ]
    home_items.insert(0, build_home_item(data, slug, page_url))
    home_data["transfers"] = home_items
    home_data["generated_at"] = datetime.now().isoformat(
        timespec="seconds"
    )
    write_json(home_data_path, home_data)

    ticker_data = load_json(ticker_data_path)
    if not isinstance(ticker_data, list):
        raise TypeError("data/transfers.json must be an array")

    ticker_items = [
        item
        for item in ticker_data
        if not entity_matches(item, data, slug, page_url)
    ]
    ticker_items.insert(0, build_ticker_item(data, slug, page_url))
    write_json(ticker_data_path, ticker_items)

    try:
        final_home = load_json(home_data_path)
        final_ticker = load_json(ticker_data_path)

        data_checks = {
            "home_single_entity":
                sum(
                    entity_matches(item, data, slug, page_url)
                    for item in final_home["transfers"]
                ) == 1,
            "ticker_single_entity":
                sum(
                    entity_matches(item, data, slug, page_url)
                    for item in final_ticker
                ) == 1,
            "homepage_status_completed":
                final_home["transfers"][0].get("status") == "completed",
            "homepage_status_display":
                final_home["transfers"][0].get("status_display")
                == "состоялся",
            "ticker_status_completed":
                final_ticker[0].get("status") == "completed",
            "ticker_status_label":
                final_ticker[0].get("status_label") == "СОСТОЯЛСЯ",
            "ticker_enabled":
                final_ticker[0].get("show_in_top_ticker") is True,
            "footer_disabled":
                final_ticker[0].get("show_in_footer_ticker") is False,
            "nested_from_club_object":
                isinstance(final_ticker[0].get("from_club"), dict),
            "nested_to_club_object":
                isinstance(final_ticker[0].get("to_club"), dict),
        }

        for name, passed in data_checks.items():
            log(f"DATA_CHECK[{name}]: {passed}")
            if not passed:
                raise RuntimeError(f"Data validation failed: {name}")

        temp = TEMP_ROOT / f"universal_import_{slug}"
        build_site(root, hugo, temp)

        home_path, home_html = locate_home(temp)
        transfer_path, transfer_html = locate_transfer(temp, slug)

        rendered_checks = {
            "homepage_transfer_visible":
                ordered_context_contains(
                    home_html,
                    "pf-home-panel--transfers",
                    str(data["player"]),
                    slug,
                ),
            "upper_ticker_visible":
                ordered_context_contains(
                    home_html,
                    "pf-ticker__item",
                    str(data["player"]),
                    slug,
                ),
            "specific_page_visible":
                str(data["player"]) in transfer_html
                and str(data["from_club"]["name"]) in transfer_html
                and str(data["to_club"]["name"]) in transfer_html,
            "agreement_label_removed":
                "СОГЛАСОВАНО" not in (
                    json.dumps(
                        final_home["transfers"][0],
                        ensure_ascii=False,
                    )
                    + json.dumps(
                        final_ticker[0],
                        ensure_ascii=False,
                    )
                ),
        }

        for name, passed in rendered_checks.items():
            log(f"RENDERED_CHECK[{name}]: {passed}")
            if not passed:
                raise RuntimeError(
                    f"Rendered validation failed: {name}"
                )

        protected_checks = {
            "upper_partial_unchanged":
                hashlib.sha256(
                    upper_partial.read_bytes()
                ).hexdigest() == upper_hash,
            "lower_partial_unchanged":
                hashlib.sha256(
                    lower_partial.read_bytes()
                ).hexdigest() == lower_hash,
        }

        for name, passed in protected_checks.items():
            log(f"PROTECTED_CHECK[{name}]: {passed}")
            if not passed:
                raise RuntimeError(
                    f"Protected template changed: {name}"
                )

        log(f"CONTENT_FILE: {content_path}")
        log(f"HOMEPAGE_DATA_FILE: {home_data_path}")
        log(f"UPPER_TICKER_DATA_FILE: {ticker_data_path}")
        log(f"RENDERED_HOMEPAGE: {home_path}")
        log(f"RENDERED_TRANSFER_PAGE: {transfer_path}")
        log("STATUS_VISIBLE: СОСТОЯЛСЯ")
        log("UPPER_TICKER_VISIBLE: True")
        log("LOWER_TICKER_ADDED: False")
        log("DUPLICATES: none")
        log("FINAL_STATUS: UNIVERSAL_TRANSFER_IMPORTED")
        return 0

    except Exception:
        for path, backup in backups.items():
            restore_path(path, backup)
        log("ROLLBACK_DONE: True")
        raise


def cli():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--report", default=str(REPORT_DEFAULT))
    args = parser.parse_args()

    try:
        code = main(Path(args.input), Path(args.report))
    except Exception as error:
        log(f"ERROR: {type(error).__name__}: {error}")
        log(traceback.format_exc())
        log("FINAL_STATUS: STOPPED_WITH_ERROR")
        code = 1

    raise SystemExit(code)


if __name__ == "__main__":
    cli()
