from __future__ import annotations

import base64
import json
import os
import shutil
import traceback
import urllib.parse
import urllib.request
from pathlib import Path

from openai import OpenAI
from openai.auth import SubjectTokenProvider

REPO = Path(__file__).resolve().parents[2]
REQ_ROOT = REPO / ".art-requests"
PENDING = REQ_ROOT / "pending"
PROCESSING = REQ_ROOT / "processing"
DONE = REQ_ROOT / "done"
FAILED = REQ_ROOT / "failed"


def github_actions_oidc_token_provider(audience: str) -> SubjectTokenProvider:
    request_url = os.environ["ACTIONS_ID_TOKEN_REQUEST_URL"]
    request_token = os.environ["ACTIONS_ID_TOKEN_REQUEST_TOKEN"]

    def get_token() -> str:
        parsed_url = urllib.parse.urlparse(request_url)
        query = dict(
            urllib.parse.parse_qsl(
                parsed_url.query,
                keep_blank_values=True,
            )
        )
        query["audience"] = audience
        url = urllib.parse.urlunparse(
            parsed_url._replace(query=urllib.parse.urlencode(query))
        )
        request = urllib.request.Request(
            url,
            headers={"Authorization": f"bearer {request_token}"},
        )
        with urllib.request.urlopen(request) as response:
            payload = json.loads(response.read().decode("utf-8"))
        token = payload.get("value")
        if not token:
            raise RuntimeError(
                "GitHub OIDC token response did not include a value."
            )
        return token

    return {"token_type": "jwt", "get_token": get_token}


def create_client() -> OpenAI:
    required = [
        "OPENAI_WIF_AUDIENCE",
        "OPENAI_IDENTITY_PROVIDER_ID",
        "OPENAI_SERVICE_ACCOUNT_ID",
        "ACTIONS_ID_TOKEN_REQUEST_URL",
        "ACTIONS_ID_TOKEN_REQUEST_TOKEN",
    ]
    missing = [name for name in required if not os.environ.get(name)]
    if missing:
        raise RuntimeError(
            "Missing OIDC/WIF environment values: " + ", ".join(missing)
        )

    return OpenAI(
        workload_identity={
            "identity_provider_id": os.environ[
                "OPENAI_IDENTITY_PROVIDER_ID"
            ],
            "service_account_id": os.environ[
                "OPENAI_SERVICE_ACCOUNT_ID"
            ],
            "provider": github_actions_oidc_token_provider(
                os.environ["OPENAI_WIF_AUDIENCE"]
            ),
        }
    )


def process_request(folder: Path, client: OpenAI) -> None:
    item_id = folder.name
    request_payload = json.loads(
        (folder / "request.json").read_text(encoding="utf-8")
    )
    player_ref = next(folder.glob("reference-player.*"))
    logo_ref = next(folder.glob("reference-logo.*"))

    PROCESSING.mkdir(parents=True, exist_ok=True)
    processing_folder = PROCESSING / item_id
    if processing_folder.exists():
        shutil.rmtree(processing_folder)
    shutil.move(str(folder), str(processing_folder))

    prompt = (
        f"Create three professional football transfer concept arts for "
        f"{request_payload['player']} joining "
        f"{request_payload['to_club']}. "
        "Image 1 is the identity reference for the football player. "
        "Preserve the same recognizable face, hairstyle, skin tone and body. "
        "Image 2 is the exact destination-club logo reference. "
        "Use that real logo as a large background graphic without changing "
        "its geometry or inventing a replacement. Dark cinematic stadium "
        "atmosphere, premium sports editorial lighting, clean 16:9 layout. "
        "No other people, no duplicate faces, no source-photo remnants, "
        "no player name, no captions, no transfer arrows, no watermarks. "
        "Return three genuinely different compositions suitable for a "
        "homepage hero slider."
    )

    with player_ref.open("rb") as player_file, logo_ref.open("rb") as logo_file:
        result = client.images.edit(
            model="gpt-image-2",
            image=[player_file, logo_file],
            prompt=prompt,
            n=3,
            size="1536x864",
            quality="high",
            input_fidelity="high",
            output_format="png",
        )

    generated: list[str] = []
    for index, image_item in enumerate(result.data[:3], start=1):
        if not image_item.b64_json:
            raise RuntimeError(
                f"Image {index} did not contain base64 output."
            )
        filename = f"candidate-0{index}.png"
        output_path = processing_folder / filename
        output_path.write_bytes(base64.b64decode(image_item.b64_json))
        generated.append(filename)

    if len(generated) != 3:
        raise RuntimeError(
            f"Expected exactly 3 images, received {len(generated)}."
        )

    (processing_folder / "request-result.json").write_text(
        json.dumps(
            {
                "item_id": item_id,
                "generated": generated,
                "authentication": "github_oidc_openai_wif",
                "model": "gpt-image-2",
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    DONE.mkdir(parents=True, exist_ok=True)
    done_folder = DONE / item_id
    if done_folder.exists():
        shutil.rmtree(done_folder)
    shutil.move(str(processing_folder), str(done_folder))


def fail_request(folder: Path, error: str) -> None:
    FAILED.mkdir(parents=True, exist_ok=True)
    target = FAILED / folder.name
    if target.exists():
        shutil.rmtree(target)
    if folder.exists():
        shutil.move(str(folder), str(target))
    else:
        target.mkdir(parents=True, exist_ok=True)
    (target / "error.json").write_text(
        json.dumps({"error": error}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def main() -> None:
    PENDING.mkdir(parents=True, exist_ok=True)
    client = create_client()
    for folder in sorted(PENDING.iterdir()):
        if not folder.is_dir():
            continue
        try:
            process_request(folder, client)
        except Exception as exc:
            processing_folder = PROCESSING / folder.name
            source = processing_folder if processing_folder.exists() else folder
            fail_request(source, str(exc) + "\n" + traceback.format_exc())
            raise


if __name__ == "__main__":
    main()
