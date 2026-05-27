from __future__ import annotations

import math
from pathlib import Path

from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[1]
ICON_ROOT = ROOT / "assets" / "icons"
ANIMATED_ROOT = ICON_ROOT / "animated"
STATIC_ROOT = ICON_ROOT / "static"
SIZE = 64
FRAME_COUNT = 16

COBALT = (9, 45, 134, 255)
GOLD = (246, 205, 116, 255)
GOLD_DARK = (183, 132, 45, 255)
IVORY = (255, 252, 244, 255)
INK = (38, 29, 23, 255)
TRANSPARENT = (0, 0, 0, 0)


def gear_polygon(cx: float, cy: float, outer: float, inner: float, teeth: int, angle: float) -> list[tuple[float, float]]:
    points = []
    for index in range(teeth * 2):
        radius = outer if index % 2 == 0 else inner
        theta = angle + index * math.pi / teeth
        points.append((cx + math.cos(theta) * radius, cy + math.sin(theta) * radius))
    return points


def draw_gear(draw: ImageDraw.ImageDraw, cx: float, cy: float, radius: float, angle: float, fill=COBALT) -> None:
    draw.polygon(gear_polygon(cx, cy, radius, radius * 0.78, 10, angle), fill=fill)
    draw.ellipse((cx - radius * 0.62, cy - radius * 0.62, cx + radius * 0.62, cy + radius * 0.62), fill=TRANSPARENT)
    draw.ellipse((cx - radius * 0.36, cy - radius * 0.36, cx + radius * 0.36, cy + radius * 0.36), outline=GOLD, width=3)
    draw.ellipse((cx - radius * 0.18, cy - radius * 0.18, cx + radius * 0.18, cy + radius * 0.18), fill=GOLD)


def save_frames(name: str, frames: list[Image.Image]) -> None:
    target = ANIMATED_ROOT / name
    target.mkdir(parents=True, exist_ok=True)
    for old_frame in target.glob("*.png"):
        old_frame.unlink()
    for index, frame in enumerate(frames):
        frame.save(target / f"frame_{index:02d}.png")
    STATIC_ROOT.mkdir(parents=True, exist_ok=True)
    frames[0].save(STATIC_ROOT / f"{name}.png")


def new_frame() -> Image.Image:
    return Image.new("RGBA", (SIZE, SIZE), TRANSPARENT)


def draw_arch(draw: ImageDraw.ImageDraw, color=COBALT) -> None:
    draw.line((18, 54, 18, 26), fill=color, width=4)
    draw.line((46, 54, 46, 26), fill=color, width=4)
    draw.arc((18, 10, 46, 42), 180, 360, fill=color, width=4)
    draw.line((13, 55, 51, 55), fill=color, width=4)
    draw.arc((23, 17, 41, 36), 180, 360, fill=GOLD, width=2)


def make_settings_frames() -> list[Image.Image]:
    frames = []
    for i in range(FRAME_COUNT):
        frame = new_frame()
        draw = ImageDraw.Draw(frame)
        draw_gear(draw, 25, 27, 16, i * math.tau / FRAME_COUNT, COBALT)
        draw_gear(draw, 41, 41, 12, -i * math.tau / FRAME_COUNT + 0.3, COBALT)
        draw.line((17, 53, 50, 53), fill=GOLD_DARK, width=2)
        frames.append(frame)
    return frames


def make_tutorial_frames() -> list[Image.Image]:
    frames = []
    for i in range(FRAME_COUNT):
        t = math.sin((i / (FRAME_COUNT - 1)) * math.pi)
        frame = new_frame()
        draw = ImageDraw.Draw(frame)
        draw.polygon([(10, 19), (30, 16), (30, 50), (10, 46)], fill=IVORY, outline=COBALT)
        draw.polygon([(34, 16), (54, 19), (54, 46), (34, 50)], fill=IVORY, outline=COBALT)
        draw.line((32, 16, 32, 51), fill=GOLD_DARK, width=2)
        for y in (26, 33, 40):
            draw.line((14, y, 26, y - 2), fill=COBALT, width=1)
            draw.line((38, y - 2, 50, y), fill=COBALT, width=1)
        page_tip_x = 34 + int(18 * (1 - t))
        page_lift = int(10 * t)
        draw.polygon(
            [(33, 18), (page_tip_x, 20 - page_lift), (page_tip_x, 45 + page_lift // 2), (33, 49)],
            fill=(255, 249, 232, 235),
            outline=GOLD_DARK,
        )
        frames.append(frame)
    return frames


def make_start_frames() -> list[Image.Image]:
    frames = []
    for i in range(FRAME_COUNT):
        t = i / (FRAME_COUNT - 1)
        frame = new_frame()
        draw = ImageDraw.Draw(frame)
        glow_alpha = int(45 + 125 * t)
        draw.polygon([(28, 25), (36, 25), (44, 53), (20, 53)], fill=(246, 205, 116, glow_alpha))
        draw_arch(draw)
        door_right = 45 - int(14 * t)
        draw.polygon([(22, 28), (door_right, 24 + int(4 * t)), (door_right, 52), (22, 52)], fill=COBALT)
        draw.line((door_right, 25, door_right, 51), fill=GOLD, width=2)
        draw.ellipse((door_right - 6, 39, door_right - 3, 42), fill=GOLD)
        frames.append(frame)
    return frames


def make_credits_frames() -> list[Image.Image]:
    frames = []
    for i in range(FRAME_COUNT):
        frame = new_frame()
        draw = ImageDraw.Draw(frame)
        for petal in range(8):
            angle = petal * math.tau / 8
            cx = 32 + math.cos(angle) * 14
            cy = 32 + math.sin(angle) * 14
            draw.ellipse((cx - 7, cy - 11, cx + 7, cy + 11), fill=COBALT, outline=GOLD)
        draw.ellipse((22, 22, 42, 42), fill=GOLD, outline=GOLD_DARK, width=2)
        draw.ellipse((27, 27, 37, 37), fill=IVORY)
        sparkle_angle = i * math.tau / FRAME_COUNT
        sx = 32 + math.cos(sparkle_angle) * 21
        sy = 32 + math.sin(sparkle_angle) * 21
        draw.line((sx - 4, sy, sx + 4, sy), fill=IVORY, width=2)
        draw.line((sx, sy - 4, sx, sy + 4), fill=IVORY, width=2)
        draw.line((sx - 3, sy - 3, sx + 3, sy + 3), fill=GOLD, width=1)
        draw.line((sx - 3, sy + 3, sx + 3, sy - 3), fill=GOLD, width=1)
        frames.append(frame)
    return frames


def make_exit_frames() -> list[Image.Image]:
    frames = []
    for i in range(FRAME_COUNT):
        t = i / (FRAME_COUNT - 1)
        frame = new_frame()
        draw = ImageDraw.Draw(frame)
        draw_arch(draw, IVORY)
        door_left = 23 + int(8 * t)
        draw.polygon([(23, 27), (43, 23), (43, 53), (door_left, 51)], fill=IVORY)
        draw.line((43, 23, 43, 53), fill=GOLD, width=2)
        arrow_end = 21 - int(9 * t)
        draw.line((38, 39, arrow_end, 39), fill=GOLD, width=4)
        draw.polygon([(arrow_end, 39), (arrow_end + 8, 32), (arrow_end + 8, 46)], fill=GOLD)
        frames.append(frame)
    return frames


def main() -> None:
    save_frames("ajustes", make_settings_frames())
    save_frames("tutorial", make_tutorial_frames())
    save_frames("comenzar", make_start_frames())
    save_frames("creditos", make_credits_frames())
    save_frames("salir", make_exit_frames())


if __name__ == "__main__":
    main()
