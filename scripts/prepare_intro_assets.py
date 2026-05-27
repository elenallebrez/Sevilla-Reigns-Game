from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
TARGET_ROOT = ROOT / "resources" / "icons" / "pygame" / "intro"
FONT_PATH = ROOT / "resources" / "fonts" / "Cinzel-Bold.ttf"

COBALT = (9, 45, 134, 255)
GOLD = (246, 205, 116, 255)
GOLD_DARK = (176, 128, 44, 255)
IVORY = (255, 252, 244, 255)
TRANSPARENT = (0, 0, 0, 0)


def text_size(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.FreeTypeFont) -> tuple[int, int]:
    bbox = draw.textbbox((0, 0), text, font=font)
    return bbox[2] - bbox[0], bbox[3] - bbox[1]


def build_no8do_emblem() -> Image.Image:
    render_scale = 3
    width = 340
    height = 150
    emblem = Image.new("RGBA", (width * render_scale, height * render_scale), TRANSPARENT)
    draw = ImageDraw.Draw(emblem)
    font = ImageFont.truetype(str(FONT_PATH), 68 * render_scale)

    text = "NO8DO"
    text_width, text_height = text_size(draw, text, font)
    text_x = (width * render_scale - text_width) // 2
    text_y = 66 * render_scale - text_height // 2
    shadow_offset = 3 * render_scale

    draw.text((text_x + shadow_offset, text_y + shadow_offset), text, font=font, fill=COBALT)
    draw.text((text_x, text_y), text, font=font, fill=GOLD)
    draw.line((42 * render_scale, 124 * render_scale, 298 * render_scale, 124 * render_scale), fill=GOLD_DARK, width=2 * render_scale)
    draw.ellipse((164 * render_scale, 118 * render_scale, 176 * render_scale, 130 * render_scale), fill=COBALT)
    return emblem.resize((width, height), Image.Resampling.LANCZOS)


def main() -> None:
    TARGET_ROOT.mkdir(parents=True, exist_ok=True)
    build_no8do_emblem().save(TARGET_ROOT / "no8do_emblem.png")


if __name__ == "__main__":
    main()
