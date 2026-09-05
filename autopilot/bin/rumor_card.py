"""
PROMYACHIK — КАРТИНКА СЛУХА ДЛЯ РЕПОСТОВ И ДЛЯ САМОЙ СТРАНИЦЫ

Зачем. Ссылку на трансфер в телеграме разворачивает крупная карточка с
портретом игрока, а ссылку на слух — голая строка: у страниц слухов нет
og:image. Дмитрий рассчитывает на сарафанку, и это прямая потеря кликов.

Что делаем. Портрет Transfermarkt приходит размером 300x390 — для крупной
карточки этого мало, мессенджеры ждут примерно 1200x630. Поэтому собираем
карточку сами: тёмный фон сайта, портрет слева, эмблемы обоих клубов со
знакомыми шевронами справа.

Текста на карточке нет намеренно. Заголовок мессенджер и так подставляет
рядом из og:title, а рисование текста потребовало бы шрифта, которого на
раннере может не оказаться: там Ubuntu, у неё свой набор, и подбирать его
вслепую — верный способ получить квадраты вместо букв.

    python rumor_card.py --slug rashford-arsenal --check
"""
from __future__ import annotations

import argparse
import io
import sys
import urllib.request
from pathlib import Path

BIN = Path(__file__).resolve().parent
sys.path.insert(0, str(BIN))
from paths import SITE  # noqa: E402

PORTRAITS = SITE / "static" / "images" / "players" / "rumors"
CARDS = SITE / "static" / "images" / "rumors" / "cards"

CARD_SIZE = (1200, 630)
BACKGROUND = (7, 9, 12)
ACCENT = (52, 208, 88)

UA = {"User-Agent": "Mozilla/5.0 (compatible; ProFutbik/1.0; +https://profutbik.ru)"}


def fetch(url: str) -> bytes:
    request = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(request, timeout=40) as response:
        return response.read()


def save_portrait(slug: str, portrait_url: str):
    """Портрет кладём себе. Ссылаться на чужой домен нельзя: адрес у
    Transfermarkt содержит метку времени и меняется при переоценке, а
    og:image с чужого хоста часть агрегаторов просто игнорирует."""
    from PIL import Image

    if not portrait_url:
        return None
    PORTRAITS.mkdir(parents=True, exist_ok=True)
    target = PORTRAITS / ("%s.jpg" % slug)
    image = Image.open(io.BytesIO(fetch(portrait_url))).convert("RGB")
    image.save(target, "JPEG", quality=88, optimize=True, progressive=True)
    return target


def _load_logo(rel_path: str):
    from PIL import Image

    if not rel_path:
        return None
    path = SITE / "static" / rel_path.lstrip("/")
    if not path.is_file():
        return None
    return Image.open(path).convert("RGBA")


def _chevrons(draw, x: int, y: int, height: int) -> None:
    """Те же три шеврона, что в списке на главной и в статье о переходе."""
    step = int(height * 0.72)
    for index in range(3):
        left = x + index * step
        fade = (0.45, 0.72, 1.0)[index]
        colour = tuple(int(channel * fade) for channel in ACCENT)
        draw.line([(left, y), (left + height // 2, y + height // 2),
                   (left, y + height)], fill=colour,
                  width=max(4, height // 7), joint="curve")


def build_card(slug: str, portrait_path, from_logo: str, to_logo: str):
    from PIL import Image, ImageDraw

    CARDS.mkdir(parents=True, exist_ok=True)
    card = Image.new("RGB", CARD_SIZE, BACKGROUND)
    draw = ImageDraw.Draw(card)

    # Тонкая золотая рамка — тот же приём, что у панелей на сайте.
    draw.rectangle([12, 12, CARD_SIZE[0] - 13, CARD_SIZE[1] - 13],
                   outline=(214, 170, 34), width=2)

    if portrait_path and Path(portrait_path).is_file():
        portrait = Image.open(portrait_path).convert("RGB")
        height = 520
        width = int(portrait.width * height / portrait.height)
        portrait = portrait.resize((width, height), Image.Resampling.LANCZOS)
        card.paste(portrait, (70, CARD_SIZE[1] - height - 55))

    # Эмблемы и стрелка — справа, на одной высоте с центром карточки.
    logo_size = 190
    centre_y = CARD_SIZE[1] // 2 - logo_size // 2
    left_x = 560
    right_x = CARD_SIZE[0] - logo_size - 90

    for rel, x in ((from_logo, left_x), (to_logo, right_x)):
        logo = _load_logo(rel)
        if logo is None:
            continue
        logo.thumbnail((logo_size, logo_size), Image.Resampling.LANCZOS)
        offset = (x + (logo_size - logo.width) // 2,
                  centre_y + (logo_size - logo.height) // 2)
        card.paste(logo, offset, logo)

    chevron_height = 54
    _chevrons(draw, left_x + logo_size + 40,
              CARD_SIZE[1] // 2 - chevron_height // 2, chevron_height)

    target = CARDS / ("%s.jpg" % slug)
    card.save(target, "JPEG", quality=90, optimize=True, progressive=True)
    return target


def make(slug: str, portrait_url: str, from_logo: str, to_logo: str) -> dict:
    """Портрет и карточка. Отказ не должен ронять публикацию слуха:
    страница без картинки хуже, чем с картинкой, но лучше, чем никакой."""
    result = {"portrait": "", "card": ""}
    try:
        portrait = save_portrait(slug, portrait_url)
        if portrait:
            result["portrait"] = "images/players/rumors/%s.jpg" % slug
        card = build_card(slug, portrait, from_logo, to_logo)
        if card:
            result["card"] = "images/rumors/cards/%s.jpg" % slug
    except Exception as error:
        print("  картинка слуха не собрана: %s" % str(error)[:90])
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Картинка для страницы слуха")
    parser.add_argument("--slug", required=True)
    parser.add_argument("--portrait", default="")
    parser.add_argument("--from-logo", default="")
    parser.add_argument("--to-logo", default="")
    args = parser.parse_args(argv)
    print(make(args.slug, args.portrait, args.from_logo, args.to_logo))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
