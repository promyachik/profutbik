from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
import shutil
import ssl
import sys
import urllib.parse
import urllib.request
import unicodedata
from collections import OrderedDict
from datetime import datetime
from io import BytesIO
from pathlib import Path

from PIL import Image, ImageFilter, ImageOps

ENGINE_VERSION = "3.4"

PROFUTBIK = Path(r"C:\Users\Dmitrii\ProFutbik")
DEFAULT_ACTIVE_PROJECT = Path(r"C:\Users\Dmitrii\Promyachik_CLEAN")

BERNARDO_REFERENCE = (
    "content/transfers/bernardo-silva-real-madrid/index.md"
)

REMOVE_KEYS = {
    "concept_art_image",
    "concept_art",
    "homepage_image",
    "hero_image",
    "card_image",
    "featured_card_image",
    "market_value_chart",
    "value_history",
    "market_value_history",
    "stats",
    "player_stats",
    "matches",
    "goals",
    "assists",
    "yellow_cards",
    "red_cards",
}

PORTRAIT_PATTERNS = (
    re.compile(
        r'https://img\.a\.transfermarkt\.technology/portrait/header/[^"\'<>\s]+',
        re.IGNORECASE,
    ),
    re.compile(
        r'https://img\.a\.transfermarkt\.technology/portrait/big/[^"\'<>\s]+',
        re.IGNORECASE,
    ),
    re.compile(
        r'https://[^"\'<>\s]+transfermarkt\.technology/portrait/[^"\'<>\s]+',
        re.IGNORECASE,
    ),
)

# PROFUTBIK_436B_ASCII_SAFE_CONSOLE_V1
# Preserve full Unicode in JSON/Markdown/site files. Only console output is
# transliterated to characters supported by the active Windows code page.
_CONSOLE_TRANSLITERATION = str.maketrans({
    "ß": "ss", "ẞ": "SS", "ø": "o", "Ø": "O",
    "ł": "l", "Ł": "L", "đ": "d", "Đ": "D",
    "ð": "d", "Ð": "D", "þ": "th", "Þ": "Th",
    "æ": "ae", "Æ": "AE", "œ": "oe", "Œ": "OE",
    "ı": "i", "İ": "I",
})


def console_safe_text(value) -> str:
    text = str(value).translate(_CONSOLE_TRANSLITERATION)
    text = unicodedata.normalize("NFKD", text)
    text = "".join(
        char for char in text
        if not unicodedata.combining(char)
    )
    encoding = getattr(sys.stdout, "encoding", None) or "utf-8"
    try:
        return text.encode(
            encoding,
            errors="replace",
        ).decode(
            encoding,
            errors="replace",
        )
    except LookupError:
        return text.encode(
            "ascii",
            errors="replace",
        ).decode("ascii")


def console_print(*values, sep: str = " ", end: str = "\\n", flush: bool = False) -> None:
    rendered = sep.join(console_safe_text(value) for value in values)
    print(rendered, end=end, flush=flush)


def configure_console_streams() -> None:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(errors="replace")
        except (AttributeError, ValueError, OSError):
            pass


configure_console_streams()


def progress(message: str) -> None:
    console_print(f"[ENGINE] {message}", flush=True)

def fail(message: str) -> None:
    progress(f"ERROR: {message}")
    raise RuntimeError(message)

def read_text(path: Path) -> str:
    raw = path.read_bytes()
    for encoding in ("utf-8-sig", "utf-8", "cp1251"):
        try:
            return raw.decode(encoding)
        except UnicodeDecodeError:
            continue
    return raw.decode("utf-8", errors="replace")

def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="")

def split_markdown(text: str) -> tuple[str, str]:
    if not text.startswith("---"):
        fail("Markdown does not start with YAML front matter")
    closing = text.find("\n---", 3)
    if closing < 0:
        fail("Closing YAML delimiter not found")
    return text[4:closing], text[closing + 4:]

def parse_top_blocks(front: str) -> OrderedDict[str, str]:
    lines = front.splitlines()
    result: OrderedDict[str, list[str]] = OrderedDict()
    current_key: str | None = None

    for line in lines:
        match = re.match(r"^([A-Za-z0-9_]+)\s*:", line)
        if match:
            current_key = match.group(1)
            result[current_key] = [line]
        elif current_key is not None:
            result[current_key].append(line)
        elif line.strip():
            fail(f"Unexpected YAML text before first key: {line!r}")

    return OrderedDict(
        (key, "\n".join(value).rstrip())
        for key, value in result.items()
    )

def scalar_block(key: str, value) -> str:
    if isinstance(value, bool):
        rendered = "true" if value else "false"
    elif isinstance(value, (int, float)):
        rendered = str(value)
    elif value is None:
        rendered = '""'
    else:
        rendered = json.dumps(str(value), ensure_ascii=False)
    return f"{key}: {rendered}"

def render_front(blocks: OrderedDict[str, str]) -> str:
    return "\n".join(blocks.values()).rstrip() + "\n"

HTTP_USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/150.0.0.0 Safari/537.36"
)


def network_headers(
    referer: str = "",
    *,
    accept_json: bool = False,
) -> dict[str, str]:
    headers = {
        "User-Agent": "Mozilla/5.0" if accept_json else HTTP_USER_AGENT,
        "Accept-Language": "en-US,en;q=0.9",
        "Accept": "application/json" if accept_json else "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    }
    if referer:
        headers["Referer"] = referer
    return headers


def fetch_with_urllib(
    url: str,
    headers: dict[str, str],
    context=None,
) -> bytes:
    request = urllib.request.Request(
        url,
        headers=headers,
    )
    kwargs = {
        "timeout": 40,
    }
    if context is not None:
        kwargs["context"] = context

    with urllib.request.urlopen(
        request,
        **kwargs,
    ) as response:
        payload = response.read()

    if not payload:
        raise RuntimeError(
            "urllib returned an empty response"
        )
    return payload


def fetch_with_certifi(
    url: str,
    headers: dict[str, str],
) -> bytes:
    try:
        import certifi
    except Exception as error:
        raise RuntimeError(
            f"certifi is unavailable: {error}"
        ) from error

    context = ssl.create_default_context(
        cafile=certifi.where()
    )
    return fetch_with_urllib(
        url,
        headers,
        context=context,
    )


def fetch_bytes(
    url: str,
    referer: str = "",
    *,
    accept_json: bool = False,
) -> bytes:
    parsed = urllib.parse.urlparse(url)
    if parsed.scheme.casefold() != "https":
        raise RuntimeError(
            f"Only HTTPS downloads are allowed: {url}"
        )

    headers = network_headers(referer, accept_json=accept_json)
    transports = (
        (
            "python-default-ca",
            lambda: fetch_with_urllib(url, headers),
        ),
        (
            "python-certifi-ca",
            lambda: fetch_with_certifi(url, headers),
        ),
    )

    errors: list[str] = []
    for transport_name, transport in transports:
        try:
            payload = transport()
            progress(
                "Secure Python HTTPS transport succeeded: "
                f"{transport_name} | "
                f"{parsed.netloc}{parsed.path}"
            )
            return payload
        except Exception as error:
            errors.append(f"{transport_name}: {error}")
            progress(
                "Secure Python HTTPS transport failed: "
                f"{transport_name} | {error}"
            )

    raise RuntimeError(
        "All safe Python HTTPS transports failed for "
        f"{url}: {' | '.join(errors)}"
    )


TRANSFERMARKT_DOMAINS = (
    "www.transfermarkt.world",
    "www.transfermarkt.com",
    "www.transfermarkt.de",
    "www.transfermarkt.at",
    "www.transfermarkt.ch",
    "www.transfermarkt.co.uk",
    "www.transfermarkt.us",
    "www.transfermarkt.com.br",
    "www.transfermarkt.pt",
    "www.transfermarkt.es",
    "www.transfermarkt.it",
    "www.transfermarkt.fr",
    "www.transfermarkt.nl",
    "www.transfermarkt.be",
    "www.transfermarkt.pl",
    "www.transfermarkt.ro",
    "www.transfermarkt.gr",
    "www.transfermarkt.dk",
    "www.transfermarkt.se",
    "www.transfermarkt.fi",
    "www.transfermarkt.ie",
    "www.transfermarkt.cz",
    "www.transfermarkt.hu",
    "www.transfermarkt.sk",
    "www.transfermarkt.si",
    "www.transfermarkt.bg",
    "www.transfermarkt.ee",
    "www.transfermarkt.lv",
    "www.transfermarkt.lt",
    "www.transfermarkt.lu",
    "www.transfermarkt.com.hr",
    "www.transfermarkt.com.mt",
    "www.transfermarkt.com.tr",
    "www.transfermarkt.co",
    "www.transfermarkt.co.kr",
    "www.transfermarkt.ru",
)


def normalize_embedded_url(value: str) -> str:
    value = html.unescape(value.strip())
    value = value.replace(r"\u002F", "/")
    value = value.replace(r"\/", "/")
    return value.strip("'\" \\")

def profile_url_candidates(profile_url: str) -> list[str]:
    parsed = urllib.parse.urlparse(profile_url)
    if not parsed.path:
        fail(f"Invalid Transfermarkt profile URL: {profile_url}")

    player_match = re.search(r"/spieler/(\d+)", parsed.path)
    if not player_match:
        fail(f"Transfermarkt player id is missing from profile URL: {profile_url}")
    player_id = player_match.group(1)

    path_variants = [
        parsed.path,
        f"/-/profil/spieler/{player_id}",
    ]

    result: list[str] = []
    for domain in TRANSFERMARKT_DOMAINS:
        for path in path_variants:
            candidate = urllib.parse.urlunparse(
                ("https", domain, path, "", "", "")
            )
            if candidate not in result:
                result.append(candidate)

    # The exact user/job URL always remains first.
    exact = urllib.parse.urlunparse(
        ("https", parsed.netloc, parsed.path, "", "", "")
    )
    if exact in result:
        result.remove(exact)
    result.insert(0, exact)
    return result

def extract_portrait_candidates(
    document: str,
    base_url: str,
) -> list[str]:
    normalized = html.unescape(document)
    normalized = normalized.replace(r"\u002F", "/")
    normalized = normalized.replace(r"\/", "/")

    found: list[str] = []

    patterns = (
        re.compile(
            r'''https?://[^"'<>\\\s,]+/portrait/
            (?:header|big|medium|small|originals?)/[^"'<>\\\s,]+''',
            re.IGNORECASE | re.VERBOSE,
        ),
        re.compile(
            r'''//[^"'<>\\\s,]+/portrait/
            (?:header|big|medium|small|originals?)/[^"'<>\\\s,]+''',
            re.IGNORECASE | re.VERBOSE,
        ),
        re.compile(
            r'''(?:src|data-src|data-original|content|href)\s*=\s*
            ["']([^"']*portrait/[^"']+)["']''',
            re.IGNORECASE | re.VERBOSE,
        ),
        re.compile(
            r'''(?:srcset|data-srcset)\s*=\s*
            ["']([^"']*portrait/[^"']+)["']''',
            re.IGNORECASE | re.VERBOSE,
        ),
    )

    for pattern in patterns:
        for match in pattern.findall(normalized):
            value = match if isinstance(match, str) else match[0]
            value = normalize_embedded_url(value)

            # srcset can contain several URL + width pairs.
            items = value.split(",") if "," in value else [value]
            for item in items:
                candidate = item.strip().split(" ")[0]
                if "portrait/" not in candidate.casefold():
                    continue
                if candidate.startswith("//"):
                    candidate = "https:" + candidate
                elif not candidate.startswith(("http://", "https://")):
                    candidate = urllib.parse.urljoin(base_url, candidate)
                candidate = candidate.rstrip("\\")
                if candidate not in found:
                    found.append(candidate)

    def rank(url: str) -> tuple[int, int]:
        lower = url.casefold()
        host = int(
            "transfermarkt.technology" in lower
            or "tmssl.akamaized.net" in lower
        )
        size = (
            5 if "/header/" in lower
            else 4 if "/big/" in lower
            else 3 if "/original" in lower
            else 2 if "/medium/" in lower
            else 1
        )
        return host, size

    found.sort(key=rank, reverse=True)
    return found

def validate_portrait_bytes(raw: bytes) -> tuple[Image.Image, tuple[int, int]]:
    try:
        image = Image.open(BytesIO(raw))
        image.load()
    except Exception as exc:
        fail(f"Downloaded portrait is not an image: {exc}")

    width, height = image.size
    if width < 100 or height < 130:
        fail(
            f"Transfermarkt portrait is too small: {width}x{height}"
        )
    return image.convert("RGBA"), (width, height)

def photo_url_variants(url: str) -> list[str]:
    result = [url]
    for old, new in (
        ("/small/", "/header/"),
        ("/medium/", "/header/"),
        ("/big/", "/header/"),
        ("/header/", "/big/"),
    ):
        if old in url:
            candidate = url.replace(old, new)
            if candidate not in result:
                result.append(candidate)
    return result

def try_photo_urls(
    urls: list[str],
    profile_url: str,
    diagnostics: list[str],
):
    attempted: set[str] = set()

    allowed_image_hosts = (
        "transfermarkt.technology",
        "tmssl.akamaized.net",
        "tmsi.akamaized.net",
    )

    for source_url in urls:
        for url in photo_url_variants(source_url):
            if url in attempted:
                continue
            attempted.add(url)
            parsed = urllib.parse.urlparse(url)
            host = parsed.netloc.casefold()
            if not any(host == allowed or host.endswith("." + allowed) for allowed in allowed_image_hosts):
                diagnostics.append(f"PHOTO_REJECT_NON_TRANSFERMARKT_HOST {url}")
                continue
            try:
                progress(f"Trying portrait candidate: {url}")
                raw = fetch_bytes(url, referer=profile_url)
                _, size = validate_portrait_bytes(raw)
                diagnostics.append(
                    f"PHOTO_OK {url} {size[0]}x{size[1]}"
                )
                progress(
                    f"Portrait accepted: {size[0]}x{size[1]}"
                )
                return url, raw, size
            except Exception as exc:
                diagnostics.append(
                    f"PHOTO_FAIL {url} {type(exc).__name__}: {exc}"
                )
    return None

def collect_transfermarkt_portrait_urls(value, player_id: int) -> list[str]:
    urls: list[str] = []

    def visit(node) -> None:
        if isinstance(node, dict):
            for key, child in node.items():
                key_cf = str(key).casefold()
                if isinstance(child, str):
                    candidate = normalize_embedded_url(child)
                    parsed = urllib.parse.urlparse(candidate)
                    host = parsed.netloc.casefold()
                    path_cf = parsed.path.casefold()
                    if (
                        parsed.scheme.casefold() == "https"
                        and "transfermarkt.technology" in host
                        and "/portrait/" in path_cf
                        and str(player_id) in candidate
                    ):
                        if candidate not in urls:
                            urls.append(candidate)
                    elif (
                        key_cf in {"imageurl", "image_url", "portraiturl", "portrait_url", "image"}
                        and parsed.scheme.casefold() == "https"
                        and "transfermarkt.technology" in host
                        and "/portrait/" in path_cf
                    ):
                        if candidate not in urls:
                            urls.append(candidate)
                visit(child)
        elif isinstance(node, list):
            for child in node:
                visit(child)
        elif isinstance(node, str):
            candidate = normalize_embedded_url(node)
            parsed = urllib.parse.urlparse(candidate)
            if (
                parsed.scheme.casefold() == "https"
                and "transfermarkt.technology" in parsed.netloc.casefold()
                and "/portrait/" in parsed.path.casefold()
                and str(player_id) in candidate
                and candidate not in urls
            ):
                urls.append(candidate)

    visit(value)
    return urls


def resolve_transfermarkt_portrait(
    job: dict,
    work_dir: Path,
) -> dict:
    profile_url = str(job["transfermarkt_profile_url"]).strip()
    player_id = int(job["transfermarkt_player_id"])
    diagnostics: list[str] = []
    work_dir.mkdir(parents=True, exist_ok=True)
    progress(
        "Photo resolver started for exact Transfermarkt player ID: "
        f"{player_id}"
    )

    exact_url = str(job.get("transfermarkt_photo_url") or "").strip()
    if exact_url:
        progress("Trying exact Transfermarkt image URL from JSON job")
        result = try_photo_urls([exact_url], profile_url, diagnostics)
        if result:
            url, raw, size = result
            return {
                "profile_url": profile_url,
                "resolved_profile_url": profile_url,
                "photo_url": url,
                "raw": raw,
                "source_size": size,
                "resolver": "exact_job_transfermarkt_url",
                "diagnostics": diagnostics,
            }

    # 1. Always use the exact official profile supplied by the job first.
    parsed_profile = urllib.parse.urlparse(profile_url)
    exact_profiles = [
        profile_url,
        urllib.parse.urlunparse((
            "https",
            parsed_profile.netloc,
            f"/-/profil/spieler/{player_id}",
            "",
            "",
            "",
        )),
    ]
    for index, candidate_profile in enumerate(exact_profiles, start=1):
        try:
            progress(
                f"Exact Transfermarkt.world profile {index}/{len(exact_profiles)}: "
                f"{candidate_profile}"
            )
            document = fetch_bytes(candidate_profile).decode(
                "utf-8", errors="replace"
            )
            write_text(work_dir / f"exact-profile-{index:02d}.html", document)
            urls = extract_portrait_candidates(document, candidate_profile)
            diagnostics.append(
                f"EXACT_PROFILE {candidate_profile} candidates={len(urls)}"
            )
            result = try_photo_urls(urls, candidate_profile, diagnostics)
            if result:
                url, raw, size = result
                return {
                    "profile_url": profile_url,
                    "resolved_profile_url": candidate_profile,
                    "photo_url": url,
                    "raw": raw,
                    "source_size": size,
                    "resolver": "exact_transfermarkt_world_profile",
                    "diagnostics": diagnostics,
                }
        except Exception as exc:
            diagnostics.append(
                f"EXACT_PROFILE_FAIL {candidate_profile} "
                f"{type(exc).__name__}: {exc}"
            )

    # 2. Official Transfermarkt JSON endpoint. It requires these exact
    # request headers; without Accept: application/json it returns HTTP 406.
    api_urls: list[str] = []
    configured_api = str(job.get("transfermarkt_data_profile_url") or "").strip()
    if configured_api:
        api_urls.append(configured_api)
    derived_api = f"https://tmapi-alpha.transfermarkt.technology/player/{player_id}"
    if derived_api not in api_urls:
        api_urls.append(derived_api)

    for index, api_url in enumerate(api_urls, start=1):
        try:
            progress(
                f"Official Transfermarkt JSON endpoint {index}/{len(api_urls)}: "
                f"{api_url}"
            )
            api_document = fetch_bytes(
                api_url,
                referer=profile_url,
                accept_json=True,
            ).decode("utf-8", errors="replace")
            write_text(
                work_dir / f"transfermarkt-data-{index:02d}.json",
                api_document,
            )
            payload = json.loads(api_document)
            urls = collect_transfermarkt_portrait_urls(payload, player_id)
            diagnostics.append(
                f"TRANSFERMARKT_JSON_API {api_url} candidates={len(urls)}"
            )
            result = try_photo_urls(urls, profile_url, diagnostics)
            if result:
                url, raw, size = result
                return {
                    "profile_url": profile_url,
                    "resolved_profile_url": api_url,
                    "photo_url": url,
                    "raw": raw,
                    "source_size": size,
                    "resolver": "official_transfermarkt_json_api",
                    "diagnostics": diagnostics,
                }
        except Exception as exc:
            diagnostics.append(
                f"TRANSFERMARKT_JSON_API_FAIL {api_url} "
                f"{type(exc).__name__}: {exc}"
            )

    # 3. Only after the exact profile and official JSON API failed, try the
    # remaining official Transfermarkt mirrors. Do not repeat the exact URLs.
    exact_set = set(exact_profiles)
    profiles = [url for url in profile_url_candidates(profile_url) if url not in exact_set]
    for index, candidate_profile in enumerate(profiles, start=1):
        try:
            progress(
                f"Fallback official Transfermarkt mirror {index}/{len(profiles)}: "
                f"{candidate_profile}"
            )
            document = fetch_bytes(candidate_profile).decode(
                "utf-8", errors="replace"
            )
            write_text(work_dir / f"fallback-profile-{index:02d}.html", document)
            urls = extract_portrait_candidates(document, candidate_profile)
            diagnostics.append(
                f"FALLBACK_PROFILE {candidate_profile} candidates={len(urls)}"
            )
            result = try_photo_urls(urls, candidate_profile, diagnostics)
            if result:
                url, raw, size = result
                return {
                    "profile_url": profile_url,
                    "resolved_profile_url": candidate_profile,
                    "photo_url": url,
                    "raw": raw,
                    "source_size": size,
                    "resolver": "fallback_official_transfermarkt_mirror",
                    "diagnostics": diagnostics,
                }
        except Exception as exc:
            diagnostics.append(
                f"FALLBACK_PROFILE_FAIL {candidate_profile} "
                f"{type(exc).__name__}: {exc}"
            )

    diagnostics_path = work_dir / "portrait-resolver-diagnostics.txt"
    write_text(diagnostics_path, "\n".join(diagnostics) + "\n")
    fail(
        "Universal Transfermarkt portrait resolver exhausted all official methods "
        f"for player ID {player_id}; diagnostics: {diagnostics_path}"
    )


def prepare_black_player_image(
    job: dict,
    output_path: Path,
    work_dir: Path,
) -> dict:
    progress("STEP 3A: resolving real Transfermarkt portrait")
    resolved = resolve_transfermarkt_portrait(job, work_dir)
    raw = resolved.pop("raw")
    progress(
        "Transfermarkt portrait resolved by: "
        + str(resolved.get("resolver"))
    )

    work_dir.mkdir(parents=True, exist_ok=True)
    source_path = work_dir / "transfermarkt-source"
    source_path.write_bytes(raw)

    source, source_size = validate_portrait_bytes(raw)

    if source.width < 120 or source.height < 150:
        fail(
            "Transfermarkt portrait is unexpectedly small: "
            f"{source.width}x{source.height}"
        )

    upscaled = False
    segmentation_input = source
    progress(
        f"Source portrait size: {source.width}x{source.height}"
    )
    if source.height < 720:
        progress("Upscaling small portrait before background removal")
        scale = 720 / source.height
        segmentation_input = source.convert("RGB").resize(
            (max(1, round(source.width * scale)), 720),
            Image.Resampling.LANCZOS,
        )
        segmentation_input = segmentation_input.filter(
            ImageFilter.UnsharpMask(
                radius=1.2,
                percent=115,
                threshold=3,
            )
        ).convert("RGBA")
        upscaled = True

    from rembg import remove

    progress(
        "STEP 3B: rembg background removal started; "
        "the first run may take several minutes"
    )
    foreground = remove(segmentation_input).convert("RGBA")
    progress("STEP 3B: rembg background removal finished")
    alpha = foreground.getchannel("A")
    bbox = alpha.getbbox()
    if not bbox:
        fail("rembg produced an empty foreground")

    foreground = foreground.crop(bbox)
    foreground = ImageOps.contain(
        foreground,
        (680, 875),
        method=Image.Resampling.LANCZOS,
    )

    canvas = Image.new("RGBA", (700, 900), (0, 0, 0, 255))
    x = (700 - foreground.width) // 2
    y = 900 - foreground.height
    canvas.alpha_composite(foreground, (x, y))

    output_path.parent.mkdir(parents=True, exist_ok=True)
    canvas.convert("RGB").save(output_path, "PNG", optimize=True)

    return {
        **resolved,
        "source_size": list(source_size),
        "upscaled_before_rembg": upscaled,
        "output_size": [700, 900],
        "background": "#000000",
        "source_file": str(source_path),
        "output_file": str(output_path),
        "engine_version": ENGINE_VERSION,
    }

def normalize_flag_token(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", str(value))
    ascii_value = "".join(
        char for char in normalized
        if not unicodedata.combining(char)
    )
    return re.sub(r"[^a-z0-9]+", "", ascii_value.lower())


def find_existing_flag(active_project: Path, job: dict) -> str:
    flag_dir = active_project / "static" / "images" / "flags"
    if not flag_dir.is_dir():
        fail(f"Nationality flag directory not found: {flag_dir}")

    aliases = job.get("nationality_flag_aliases")
    if not isinstance(aliases, list) or not aliases:
        fail("nationality_flag_aliases must be a non-empty list")

    raw_tokens = [
        job["nationality_code"],
        job["nationality_fifa_code"],
        job["nationality"],
        *aliases,
    ]
    tokens = {
        normalize_flag_token(value)
        for value in raw_tokens
        if str(value).strip()
    }
    tokens.discard("")
    if not tokens:
        fail("Nationality flag search tokens are empty")

    allowed = {".svg", ".png", ".webp", ".jpg", ".jpeg"}
    files = sorted(
        (
            path for path in flag_dir.rglob("*")
            if path.is_file()
            and path.suffix.lower() in allowed
        ),
        key=lambda path: (
            0 if path.suffix.lower() == ".svg" else 1,
            len(path.relative_to(flag_dir).parts),
            str(path).lower(),
        ),
    )

    progress(
        "Searching existing nationality assets recursively: "
        f"{len(files)} files | tokens={sorted(tokens)}"
    )

    for path in files:
        if normalize_flag_token(path.stem) in tokens:
            rel = path.relative_to(
                active_project / "static"
            ).as_posix()
            progress(f"Existing nationality flag selected: {rel}")
            return rel

    for path in files:
        relative = path.relative_to(flag_dir)
        normalized_parts = {
            normalize_flag_token(part)
            for part in relative.parts
        }
        if normalized_parts & tokens:
            rel = path.relative_to(
                active_project / "static"
            ).as_posix()
            progress(f"Existing nationality flag selected: {rel}")
            return rel

    long_tokens = sorted(
        (token for token in tokens if len(token) >= 3),
        key=len,
        reverse=True,
    )
    for path in files:
        normalized_relative = normalize_flag_token(
            path.relative_to(flag_dir).as_posix()
        )
        if any(token in normalized_relative for token in long_tokens):
            rel = path.relative_to(
                active_project / "static"
            ).as_posix()
            progress(f"Existing nationality flag selected: {rel}")
            return rel

    sample = ", ".join(
        path.relative_to(flag_dir).as_posix()
        for path in files[:40]
    )
    fail(
        "Existing nationality flag was not matched. "
        f"Scanned {len(files)} files recursively; "
        f"tokens={sorted(tokens)}; first files={sample}"
    )

def find_playerdb_id(active_project: Path, player_name: str) -> int | None:
    path = active_project / "data" / "playerdb" / "players.json"
    if not path.is_file():
        return None

    try:
        payload = json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception:
        return None

    normalized = player_name.casefold()

    def walk(value):
        if isinstance(value, dict):
            name = str(
                value.get("name")
                or value.get("player_name")
                or ""
            ).strip()
            if name.casefold() == normalized:
                for key in ("id", "player_id", "api_id"):
                    candidate = value.get(key)
                    if isinstance(candidate, int):
                        return candidate
                    if isinstance(candidate, str) and candidate.isdigit():
                        return int(candidate)
            for child in value.values():
                found = walk(child)
                if found is not None:
                    return found
        elif isinstance(value, list):
            for child in value:
                found = walk(child)
                if found is not None:
                    return found
        return None

    return walk(payload)

def inspect_club_logo_file(path: Path) -> dict:
    if not path.is_file():
        raise RuntimeError(f"Club logo file does not exist: {path}")
    if path.stat().st_size < 256:
        raise RuntimeError(
            f"Club logo file is too small: {path} "
            f"({path.stat().st_size} bytes)"
        )

    try:
        with Image.open(path) as image:
            image.load()
            width, height = image.size
            image_format = str(image.format or "").upper()
    except Exception as error:
        raise RuntimeError(
            f"Club logo cannot be decoded: {path}: {error}"
        ) from error

    if image_format != "PNG":
        raise RuntimeError(
            f"Club logo is not PNG: {path} format={image_format}"
        )
    if width < 32 or height < 32:
        raise RuntimeError(
            f"Club logo dimensions are too small: "
            f"{path} size={width}x{height}"
        )

    return {
        "path": str(path),
        "format": image_format,
        "width": width,
        "height": height,
        "bytes": path.stat().st_size,
    }


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def publish_versioned_club_logo(
    active_project: Path,
    source_path: Path,
    club_id: int,
) -> str:
    digest = file_sha256(source_path)
    relative = (
        Path("images")
        / "clubs"
        / "api"
        / "rendered"
        / f"{club_id}-{digest[:12]}.png"
    )
    target = active_project / "static" / relative
    target.parent.mkdir(parents=True, exist_ok=True)

    if (
        not target.is_file()
        or file_sha256(target) != digest
    ):
        shutil.copy2(source_path, target)

    target_info = inspect_club_logo_file(target)
    if file_sha256(target) != digest:
        raise RuntimeError(
            f"Versioned club logo hash mismatch: {target}"
        )

    progress(
        "Versioned club logo ready: "
        f"{relative.as_posix()} | "
        f"{target_info['width']}x{target_info['height']}"
    )
    return relative.as_posix()


def update_club_logo_catalog(
    active_project: Path,
    club_id: int,
    club_name: str,
    logo_rel: str,
) -> None:
    catalog_path = active_project / "data" / "club-logos.json"
    if not catalog_path.is_file():
        raise RuntimeError(f"Club logo catalog missing: {catalog_path}")

    payload = json.loads(catalog_path.read_text(encoding="utf-8-sig"))
    if not isinstance(payload, dict) or not isinstance(payload.get("clubs"), dict):
        raise RuntimeError("data/club-logos.json has invalid structure")

    clubs = payload["clubs"]
    key = str(club_id)
    record = clubs.get(key)
    if not isinstance(record, dict):
        record = {"id": club_id, "name": club_name}
        clubs[key] = record

    record["id"] = club_id
    record["name"] = str(record.get("name") or club_name)
    record["configured_name"] = club_name
    record["logo"] = logo_rel
    record["api_logo"] = (
        "https://media.api-sports.io/football/teams/"
        f"{club_id}.png"
    )
    record["logo_validation"] = {
        "mode": "content_hashed_local_png",
        "engine_version": ENGINE_VERSION,
    }

    write_text(
        catalog_path,
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
    )

    reread = json.loads(catalog_path.read_text(encoding="utf-8-sig"))
    actual = reread["clubs"][key].get("logo")
    if actual != logo_rel:
        raise RuntimeError(
            f"Club logo catalog update failed for {club_id}: {actual}"
        )

    progress(
        f"Club logo catalog updated: {club_name} | "
        f"API id {club_id} | {logo_rel}"
    )


def club_catalog_logo_candidate(
    active_project: Path,
    club_id: int,
) -> Path | None:
    catalog_path = (
        active_project
        / "data"
        / "club-logos.json"
    )
    if not catalog_path.is_file():
        return None

    try:
        payload = json.loads(
            catalog_path.read_text(
                encoding="utf-8-sig"
            )
        )
        logo_rel = (
            payload
            .get("clubs", {})
            .get(str(club_id), {})
            .get("logo")
        )
    except Exception:
        return None

    if not isinstance(logo_rel, str):
        return None

    logo_rel = logo_rel.strip().lstrip("/")
    if not logo_rel:
        return None
    return active_project / "static" / logo_rel


def find_existing_club_logo(
    active_project: Path,
    club_id: int,
) -> Path | None:
    candidates: list[Path] = []

    catalog_candidate = club_catalog_logo_candidate(
        active_project,
        club_id,
    )
    if catalog_candidate is not None:
        candidates.append(catalog_candidate)

    clubs_root = (
        active_project
        / "static"
        / "images"
        / "clubs"
    )
    if clubs_root.is_dir():
        exact_name = f"{club_id}.png"
        version_prefix = f"{club_id}-"
        for candidate in sorted(
            clubs_root.rglob("*.png")
        ):
            name = candidate.name.casefold()
            if (
                name == exact_name.casefold()
                or name.startswith(
                    version_prefix.casefold()
                )
            ):
                candidates.append(candidate)

    seen: set[str] = set()
    for candidate in candidates:
        key = str(candidate).casefold()
        if key in seen:
            continue
        seen.add(key)

        try:
            inspect_club_logo_file(candidate)
            return candidate
        except Exception:
            continue
    return None


def verify_club_logo(
    active_project: Path,
    club_id: int,
    club_name: str,
) -> str:
    path = (
        active_project
        / "static"
        / "images"
        / "clubs"
        / "api"
        / f"{club_id}.png"
    )

    try:
        info = inspect_club_logo_file(path)
        progress(
            f"Valid club logo: {club_name} | API id {club_id} | "
            f"{info['width']}x{info['height']}"
        )
    except Exception as validation_error:
        progress(
            f"Club logo missing or invalid: {club_name} | "
            f"API id {club_id} | {validation_error}"
        )

        existing_candidate = find_existing_club_logo(
            active_project,
            club_id,
        )
        if (
            existing_candidate is not None
            and existing_candidate != path
        ):
            path.parent.mkdir(
                parents=True,
                exist_ok=True,
            )
            shutil.copy2(
                existing_candidate,
                path,
            )
            info = inspect_club_logo_file(path)
            progress(
                "Existing validated club logo reused: "
                f"{club_name} | API id {club_id} | "
                f"{existing_candidate}"
            )
        else:
            logo_url = (
                "https://media.api-sports.io/football/teams/"
                f"{club_id}.png"
            )
            progress(
                f"Refreshing official API-Football club logo: {logo_url}"
            )

            try:
                raw = fetch_bytes(logo_url)
            except Exception as error:
                fail(
                    f"Cannot download official logo for {club_name} "
                    f"(API id {club_id}): {error}"
                )

            path.parent.mkdir(parents=True, exist_ok=True)
            temp_path = path.with_name(
                f"{path.stem}.download-"
                f"{datetime.now().strftime('%Y%m%d%H%M%S')}.png"
            )
            temp_path.write_bytes(raw)

            try:
                inspect_club_logo_file(temp_path)
                temp_path.replace(path)
                info = inspect_club_logo_file(path)
            except Exception:
                if temp_path.exists():
                    temp_path.unlink()
                raise

            progress(
                f"Official club logo refreshed: {club_name} | "
                f"API id {club_id} | "
                f"{info['width']}x{info['height']} | "
                f"{info['bytes']} bytes"
            )

    logo_rel = publish_versioned_club_logo(
        active_project,
        path,
        club_id,
    )
    update_club_logo_catalog(
        active_project,
        club_id,
        club_name,
        logo_rel,
    )
    return logo_rel


def slugify_player_name(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value)
    ascii_value = normalized.encode(
        "ascii",
        errors="ignore",
    ).decode("ascii")
    slug = re.sub(
        r"[^a-z0-9]+",
        "-",
        ascii_value.casefold(),
    ).strip("-")
    if not slug:
        raise RuntimeError(
            f"Cannot derive player slug from {value!r}"
        )
    return slug


def derive_player_initials(value: str) -> str:
    parts = [
        part
        for part in re.split(r"\s+", value.strip())
        if part
    ]
    initials = "".join(part[0] for part in parts[:2]).upper()
    return initials or "PF"




def module_enabled(job: dict, name: str) -> bool:
    raw = job.get("enabled_modules")
    if raw is None:
        return True
    if not isinstance(raw, list):
        fail("enabled_modules must be a list")
    return name in {str(value).strip() for value in raw}


def build_page(
    active_project: Path,
    job: dict,
    image_rel: str,
    photo_info: dict,
) -> Path:
    reference = active_project / BERNARDO_REFERENCE
    if not reference.is_file():
        fail(f"Bernardo reference page not found: {reference}")

    playerdb_id = find_playerdb_id(
        active_project,
        job["player"],
    )
    player_id = (
        playerdb_id
        if playerdb_id is not None
        else int(job["transfermarkt_player_id"])
    )

    from_logo = verify_club_logo(
        active_project,
        int(job["from_club_id"]),
        job["from_club_name"],
    )
    to_logo = verify_club_logo(
        active_project,
        int(job["to_club_id"]),
        job["to_club_name"],
    )
    nationality_flag = find_existing_flag(
        active_project,
        job,
    )

    player_name = str(job["player"]).strip()
    player_slug = str(
        job.get("player_slug")
        or slugify_player_name(player_name)
    )
    full_name = str(
        job.get("full_name")
        or player_name
    )
    initials = str(
        job.get("player_initials")
        or derive_player_initials(player_name)
    )
    source_name = str(
        job.get("source_name")
        or "Transfermarkt"
    )
    source_url = str(
        job.get("source_url")
        or job["transfermarkt_profile_url"]
    )

    # The page is intentionally built from a clean front matter dictionary.
    # No Bernardo player/club/nationality/fee values are inherited.
    updates = OrderedDict([
        ("title", job["title"]),
        (
            "seo_title",
            str(job.get("seo_title") or job["title"]),
        ),
        ("description", job["description"]),
        (
            "date",
            datetime.now().astimezone().isoformat(
                timespec="seconds"
            ),
        ),
        (
            "lastmod",
            datetime.now().astimezone().isoformat(
                timespec="seconds"
            ),
        ),
        ("draft", bool(job.get("draft", True))),
        ("type", "transfers"),
        ("layout", "single"),
        ("test_mode", bool(job.get("test_mode", True))),
        ("pipeline_generated", True),
        ("player", player_name),
        ("player_name", player_name),
        ("full_name", full_name),
        ("player_initials", initials),
        ("player_slug", player_slug),
        ("player_id", player_id),
        (
            "transfermarkt_player_id",
            int(job["transfermarkt_player_id"]),
        ),
        ("status", job["status"]),
        ("status_label", job["status_label"]),
        ("fee", job["fee"]),
        ("amount", job["fee"]),
        ("transfer_fee", job["fee"]),
        ("from_club_id", int(job["from_club_id"])),
        ("from_club_name", job["from_club_name"]),
        ("from_club_logo", from_logo),
        ("from_logo", from_logo),
        ("from_name", job["from_club_name"]),
        ("from_team", job["from_club_name"]),
        ("to_club_id", int(job["to_club_id"])),
        ("to_club_name", job["to_club_name"]),
        ("to_club_logo", to_logo),
        ("to_logo", to_logo),
        ("to_name", job["to_club_name"]),
        ("to_team", job["to_club_name"]),
        ("player_image", image_rel),
        ("ticker_image", image_rel),
        ("cutout_player_image", image_rel),
        ("api_player_image", image_rel),
        ("player_image_fallback", image_rel),
        ("player_image_source_name", "Transfermarkt"),
        (
            "player_image_source_url",
            job["transfermarkt_profile_url"],
        ),
        (
            "transfermarkt_photo_url",
            photo_info["photo_url"],
        ),
        ("player_image_background_removed", True),
        ("player_image_black_background", True),
        ("player_image_processor", "rembg"),
        ("position", job["position"]),
        ("position_ru", job["position_ru"]),
        ("main_position", job["main_position"]),
        ("birth_date", job["birth_date"]),
        ("age", int(job["age"])),
        ("age_at_transfer", int(job["age"])),
        ("nationality", job["nationality"]),
        ("nationality_ru", job["nationality_ru"]),
        ("nationality_name", job["nationality_ru"]),
        ("nationality_flag", nationality_flag),
        ("nationality_flag_image", nationality_flag),
        ("preferred_foot", job["preferred_foot"]),
        ("market_value", job["market_value"]),
        (
            "market_value_display",
            job["market_value_display"],
        ),
        (
            "player_market_value_display",
            job["market_value_display"],
        ),
        (
            "player_brief_market_value_display",
            job["market_value_display"],
        ),
        (
            "market_value_url",
            f"/transfers/{job['slug']}/#market-value",
        ),
        ("show_in_top_ticker", module_enabled(job, "upper_ticker")),
        ("show_in_footer_ticker", module_enabled(job, "lower_ticker")),
        ("show_in_transfers_page", module_enabled(job, "homepage_transfer")),
        ("source_name", source_name),
        ("source_url", source_url),
        (
            "source_status",
            str(job.get("source_status") or "official"),
        ),
    ])

    blocks: OrderedDict[str, str] = OrderedDict()
    for key, value in updates.items():
        blocks[key] = scalar_block(key, value)

    page_text = (
        "---\n"
        + render_front(blocks)
        + "---\n\n"
        + job["seo_body_md"].strip()
        + "\n"
    )

    target = (
        active_project
        / "content"
        / "transfers"
        / job["slug"]
        / "index.md"
    )
    write_text(target, page_text)
    return target


def build_transfer_record(
    active_project: Path,
    job: dict,
    image_rel: str,
) -> dict:
    from_logo = verify_club_logo(
        active_project,
        int(job["from_club_id"]),
        job["from_club_name"],
    )
    to_logo = verify_club_logo(
        active_project,
        int(job["to_club_id"]),
        job["to_club_name"],
    )
    playerdb_id = find_playerdb_id(
        active_project,
        job["player"],
    )
    player_id = (
        playerdb_id
        if playerdb_id is not None
        else int(job["transfermarkt_player_id"])
    )

    return {
        "entity_id": (
            f"{job['slug']}__"
            f"{job['from_club_id']}__{job['to_club_id']}"
        ),
        "slug": job["slug"],
        "url": f"transfers/{job['slug']}/",
        "date": datetime.now().astimezone().isoformat(
            timespec="seconds"
        ),
        "player": job["player"],
        "player_id": player_id,
        "transfermarkt_player_id": int(
            job["transfermarkt_player_id"]
        ),
        "status": job["status"],
        "status_label": job["status_label"],
        "fee": job["fee"],
        "from_club_id": int(job["from_club_id"]),
        "from_club_name": job["from_club_name"],
        "from_club_logo": from_logo,
        "to_club_id": int(job["to_club_id"]),
        "to_club_name": job["to_club_name"],
        "to_club_logo": to_logo,
        "from_club": {
            "id": int(job["from_club_id"]),
            "name": job["from_club_name"],
            "configured_name": job["from_club_name"],
            "logo": from_logo,
        },
        "to_club": {
            "id": int(job["to_club_id"]),
            "name": job["to_club_name"],
            "configured_name": job["to_club_name"],
            "logo": to_logo,
        },
        "player_image": image_rel,
        "ticker_image": image_rel,
        "cutout_player_image": image_rel,
        "player_image_fallback": image_rel,
        "player_image_source_name": "Transfermarkt",
        "player_image_source_url": (
            job["transfermarkt_profile_url"]
        ),
        "player_image_background_removed": True,
        "player_image_black_background": True,
        "player_image_processor": "rembg",
        "nationality": job["nationality"],
        "nationality_ru": job["nationality_ru"],
        "nationality_flag": find_existing_flag(
            active_project,
            job,
        ),
        "show_in_top_ticker": module_enabled(job, "upper_ticker"),
        "show_in_footer_ticker": module_enabled(job, "lower_ticker"),
        "show_in_transfers_page": module_enabled(job, "homepage_transfer"),
        "homepage_section": "transfers",
        "kind": "transfer",
        "category": "transfer",
        "pipeline_generated": True,
        "test_mode": bool(job.get("test_mode", True)),
    }

def update_transfers_data(
    active_project: Path,
    job: dict,
    image_rel: str,
) -> Path:
    path = active_project / "data" / "transfers.json"
    if not path.is_file():
        fail(f"Transfers data not found: {path}")

    data = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(data, list):
        fail("data/transfers.json must be a list")

    record = build_transfer_record(
        active_project,
        job,
        image_rel,
    )

    cleaned = [
        item
        for item in data
        if not (
            isinstance(item, dict)
            and item.get("slug") == job["slug"]
        )
    ]
    write_text(
        path,
        json.dumps(
            cleaned + [record],
            ensure_ascii=False,
            indent=2,
        ) + "\n",
    )
    return path

def homepage_transfer_record(
    active_project: Path,
    job: dict,
) -> dict:
    from_logo = verify_club_logo(
        active_project,
        int(job["from_club_id"]),
        job["from_club_name"],
    )
    to_logo = verify_club_logo(
        active_project,
        int(job["to_club_id"]),
        job["to_club_name"],
    )

    now = datetime.now().astimezone()
    status = str(job.get("status") or "agreement")
    status_map = {
        "official": ("состоялся", "is-done"),
        "completed": ("состоялся", "is-done"),
        "confirmed": ("подтверждено", "is-done"),
        "agreement": ("переходит", "is-agreement"),
        "negotiations": ("переговоры", "is-talks"),
        "rumour": ("слух", "is-rumor"),
        "rumor": ("слух", "is-rumor"),
    }
    status_display, status_css = status_map.get(
        status,
        ("переходит", "is-agreement"),
    )

    return {
        "entity_id": (
            f"{job['slug']}__"
            f"{job['from_club_id']}__"
            f"{job['to_club_id']}"
        ),
        "date": now.isoformat(timespec="seconds"),
        "fee": str(job.get("fee") or "Сумма не указана"),
        "from_club_id": str(job["from_club_id"]),
        "from_club_name_en": job["from_club_name"],
        "from_logo": from_logo,
        "from_name": job["from_club_name"],
        "group": "transfer",
        "parser_generated": True,
        "pipeline_generated": True,
        "player": job["player"],
        "player_name_en": job["player"],
        "slug": job["slug"],
        "sort_ts": now.timestamp(),
        "status": status,
        "status_css": status_css,
        "status_display": status_display,
        "test_mode": bool(job.get("test_mode", False)),
        "title": job["title"],
        "to_club_id": str(job["to_club_id"]),
        "to_club_name_en": job["to_club_name"],
        "to_logo": to_logo,
        "to_name": job["to_club_name"],
        "url": f"transfers/{job['slug']}/",
    }


def update_homepage_transfer_block(
    active_project: Path,
    job: dict,
) -> Path:
    path = (
        active_project
        / "data"
        / "homepage_transfer_rumor.json"
    )
    if not path.is_file():
        fail(
            "Real homepage Transfers data source not found: "
            f"{path}"
        )

    payload = json.loads(
        path.read_text(encoding="utf-8-sig")
    )
    if not isinstance(payload, dict):
        fail("homepage_transfer_rumor.json must be an object")

    transfers = payload.get("transfers")
    if not isinstance(transfers, list):
        fail(
            "homepage_transfer_rumor.json field "
            "'transfers' must be a list"
        )

    record = homepage_transfer_record(
        active_project,
        job,
    )
    cleaned = [
        item
        for item in transfers
        if not (
            isinstance(item, dict)
            and item.get("slug") == job["slug"]
        )
    ]

    payload["generated_at"] = (
        datetime.now()
        .astimezone()
        .isoformat(timespec="seconds")
    )
    payload["transfers"] = [record] + cleaned

    write_text(
        path,
        json.dumps(
            payload,
            ensure_ascii=False,
            indent=2,
        ) + "\n",
    )
    return path


def verify_image(path: Path) -> dict:
    with Image.open(path) as image:
        rgb = image.convert("RGB")
        if rgb.size != (700, 900):
            fail(f"Final image size is {rgb.size}, expected 700x900")

        corners = [
            rgb.getpixel((0, 0)),
            rgb.getpixel((rgb.width - 1, 0)),
            rgb.getpixel((0, rgb.height - 1)),
            rgb.getpixel((rgb.width - 1, rgb.height - 1)),
        ]
        black_corners = sum(
            1 for pixel in corners if max(pixel) <= 15
        )
        if black_corners < 3:
            fail(f"Black background check failed: {corners}")

        sample = rgb.resize((70, 90))
        non_black = sum(
            1 for pixel in sample.getdata()
            if max(pixel) > 25
        )
        ratio = non_black / (70 * 90)
        if ratio < 0.015:
            fail("Final image appears empty")

        return {
            "width": rgb.width,
            "height": rgb.height,
            "black_corners": black_corners,
            "non_black_sample_ratio": round(ratio, 4),
        }

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("job_json")
    parser.add_argument(
        "--active-project",
        default=str(DEFAULT_ACTIVE_PROJECT),
    )
    args = parser.parse_args(argv)

    job_path = Path(args.job_json)
    active_project = Path(args.active_project)
    job = json.loads(
        job_path.read_text(encoding="utf-8-sig")
    )

    required = [
        "slug",
        "player",
        "transfermarkt_player_id",
        "transfermarkt_profile_url",
        "from_club_id",
        "from_club_name",
        "to_club_id",
        "to_club_name",
        "title",
        "description",
        "status",
        "status_label",
        "fee",
        "position",
        "position_ru",
        "main_position",
        "birth_date",
        "age",
        "nationality",
        "nationality_ru",
        "nationality_code",
        "nationality_fifa_code",
        "nationality_flag_aliases",
        "preferred_foot",
        "market_value",
        "market_value_display",
        "seo_body_md",
    ]
    missing = [key for key in required if key not in job]
    if missing:
        fail(f"Job fields missing: {missing}")

    image_rel = (
        "images/players/transfermarkt/"
        f"{job['slug']}-{job['transfermarkt_player_id']}-black.png"
    )
    image_path = active_project / "static" / image_rel
    work_dir = (
        PROFUTBIK
        / "assets-inbox"
        / job["slug"]
    )

    # Universal atomic order: resolve/process photo before page/data.
    photo_info = prepare_black_player_image(
        job,
        image_path,
        work_dir,
    )
    image_check = verify_image(image_path)
    progress(
        "STEP 3C: final image validation passed "
        f"({image_check['width']}x{image_check['height']})"
    )

    progress("STEP 3D: creating SEO transfer page")
    page_path = build_page(
        active_project,
        job,
        image_rel,
        photo_info,
    )
    progress(
        "STEP 2: updating upper ticker data"
    )
    data_path = update_transfers_data(
        active_project,
        job,
        image_rel,
    )
    progress(
        "STEP 1: updating the real homepage Transfers block data"
    )
    homepage_data_path = update_homepage_transfer_block(
        active_project,
        job,
    )
    progress("All source changes completed")

    result = {
        "slug": job["slug"],
        "player": job["player"],
        "image_rel": image_rel,
        "image_path": str(image_path),
        "image_check": image_check,
        "photo_info": photo_info,
        "page_path": str(page_path),
        "data_path": str(data_path),
        "homepage_data_path": str(homepage_data_path),
        "steps": [
            label
            for module, label in (
                ("homepage_transfer", "homepage_transfers_block"),
                ("upper_ticker", "clickable_upper_ticker"),
                ("player_page", "seo_page_and_black_background_transfermarkt_photo"),
                ("lower_ticker", "lower_footer_ticker"),
            )
            if module_enabled(job, module)
        ],
    }

    result_path = (
        PROFUTBIK
        / "reports"
        / f"transfer-news-4-step-{job['slug']}-result.json"
    )
    write_text(
        result_path,
        json.dumps(
            result,
            ensure_ascii=False,
            indent=2,
        ) + "\n",
    )

    console_print("decision: transfer_news_4_step_pipeline_applied")
    console_print("engine_version:", ENGINE_VERSION)
    console_print("photo_resolver:", photo_info.get("resolver"))
    console_print("resolved_profile_url:", photo_info.get("resolved_profile_url"))
    console_print("photo_url:", photo_info.get("photo_url"))
    console_print("page:", page_path)
    console_print("image:", image_path)
    console_print("data:", data_path)
    console_print("homepage_transfers_data:", homepage_data_path)
    console_print("result:", result_path)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
