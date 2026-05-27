from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pygame

import config


CATEGORY_TABS = (
    ("religion", "cross_cobalt.png"),
    ("people", "flamenca_cobalt.png"),
    ("money", "euro_cobalt.png"),
    ("army", "suitcases_cobalt.png"),
)

TEXT_LINE_SPACING = 5
TEXT_OVERFLOW_SUFFIX = "..."
PANEL_WIDTH_RATIO = 0.74
PANEL_HEIGHT_RATIO = 0.70
PANEL_MAX_WIDTH = 1160
PANEL_RADIUS = 20
PANEL_OUTER_BORDER_WIDTH = 4
PANEL_PADDING_X = 68
PANEL_TOP_PADDING = 28
PANEL_BOTTOM_PADDING = 56
TITLE_IMAGE_GAP = 22
IMAGE_WIDTH_RATIO = 0.66
IMAGE_HEIGHT_RATIO = 0.40
IMAGE_RADIUS = 13
DESCRIPTION_HEIGHT = 58
BUTTON_HEIGHT = 58
BUTTON_GAP = 34
BUTTON_HOVER_EASING = 0.15
BUTTON_HOVER_LIFT = 5

PANEL_FILL = (255, 249, 232)
PANEL_INNER_FILL = (255, 252, 244)
PANEL_SHADOW = (45, 35, 24)
COBALT = config.BLUE_AZULEJO
GOLD = config.ALBERO
GOLD_DARK = (176, 128, 44)
IVORY = config.CAL_WHITE
INK = config.INK
WARM_GRAY = (98, 86, 75)
BLUE_GRAY = (48, 64, 95)
MUTED_COBALT = (52, 78, 128)
PRIMARY_BUTTON_FILL = COBALT
SECONDARY_BUTTON_FILL = (255, 252, 244)

_event_image_cache: dict[str, pygame.Surface] = {}
_scaled_event_image_cache: dict[tuple[str, int, int], pygame.Surface] = {}
_category_icon_cache: dict[str, pygame.Surface] = {}
_button_hover_progress = [0.0, 0.0]


@dataclass(frozen=True)
class EventLayout:
    panel_rect: pygame.Rect
    title_y: int
    image_rect: pygame.Rect
    description_rect: pygame.Rect
    left_button_rect: pygame.Rect
    right_button_rect: pygame.Rect
    tab_rects: tuple[pygame.Rect, ...]


def get_scaled_event_image(image_name: str, max_width: int, max_height: int):
    cache_key = (image_name, max_width, max_height)
    if cache_key in _scaled_event_image_cache:
        return _scaled_event_image_cache[cache_key]

    if image_name not in _event_image_cache:
        image_path = config.IMG_PATH / image_name
        _event_image_cache[image_name] = _load_event_image(image_path)

    image = _event_image_cache[image_name]
    original_width, original_height = image.get_size()
    scale = min(max_width / original_width, max_height / original_height)
    new_size = (max(1, int(original_width * scale)), max(1, int(original_height * scale)))
    scaled_image = pygame.transform.smoothscale(image, new_size)
    _scaled_event_image_cache[cache_key] = scaled_image
    return scaled_image


def draw_text_wrapped(surface, text: str, font, color, rect, line_spacing: int = TEXT_LINE_SPACING) -> int:
    words = text.split(" ")
    lines = []
    current_line = ""

    for word in words:
        test_line = current_line + word + " "
        if font.size(test_line)[0] <= rect.width:
            current_line = test_line
            continue

        lines.append(current_line.strip())
        current_line = word + " "

    lines.append(current_line.strip())

    line_height = font.get_linesize() + line_spacing
    max_lines = max(1, rect.height // line_height)

    if len(lines) > max_lines:
        lines = lines[:max_lines]
        lines[-1] = _fit_line_with_suffix(lines[-1], font, rect.width)

    total_height = len(lines) * font.get_linesize() + max(0, len(lines) - 1) * line_spacing
    y = rect.y + max(0, (rect.height - total_height) // 2)
    for line in lines:
        rendered_text = font.render(line, True, color)
        surface.blit(rendered_text, (rect.x + (rect.width - rendered_text.get_width()) // 2, y))
        y += rendered_text.get_height() + line_spacing

    return y - rect.y


def draw_event(screen, event, swipe_offset: int, game_state=None) -> None:
    layout = _build_layout(screen, swipe_offset)

    _draw_category_tabs(screen, layout.tab_rects, game_state)
    _draw_event_panel(screen, layout.panel_rect)
    _draw_event_title(screen, event.title, layout.panel_rect, layout.title_y)
    _draw_event_image(screen, event.image, layout.panel_rect, layout.image_rect)
    _draw_event_description(screen, event.description, layout.description_rect)
    _draw_choice_buttons(screen, event.options[0].text, event.options[1].text, layout)


def get_choice_index_at_pos(screen: pygame.Surface, pos: tuple[int, int], swipe_offset: int = 0) -> int | None:
    layout = _build_layout(screen, swipe_offset)
    if layout.left_button_rect.collidepoint(pos):
        return 0
    if layout.right_button_rect.collidepoint(pos):
        return 1
    return None


def _build_layout(screen: pygame.Surface, swipe_offset: int = 0) -> EventLayout:
    width = screen.get_width()
    height = screen.get_height()

    tab_rects = _category_tab_rects(width, height)
    panel_width = min(PANEL_MAX_WIDTH, int(width * PANEL_WIDTH_RATIO))
    panel_y = tab_rects[0].bottom + int(height * 0.028)
    panel_height = min(int(height * PANEL_HEIGHT_RATIO), height - panel_y - 30)
    panel_height = max(440, panel_height)
    panel_rect = pygame.Rect((width - panel_width) // 2 + swipe_offset, panel_y, panel_width, panel_height)

    title_y = panel_rect.y + PANEL_TOP_PADDING
    image_width = int(panel_rect.width * IMAGE_WIDTH_RATIO)
    image_height = int(panel_rect.height * IMAGE_HEIGHT_RATIO)
    image_y = title_y + config.FONT_EVENT_TITLE.get_height() + TITLE_IMAGE_GAP
    image_rect = pygame.Rect(0, image_y, image_width, image_height)
    image_rect.centerx = panel_rect.centerx

    description_rect = pygame.Rect(
        panel_rect.x + PANEL_PADDING_X,
        image_rect.bottom + 18,
        panel_rect.width - PANEL_PADDING_X * 2,
        DESCRIPTION_HEIGHT,
    )

    button_width = (panel_rect.width - PANEL_PADDING_X * 2 - BUTTON_GAP) // 2
    buttons_y = panel_rect.bottom - PANEL_BOTTOM_PADDING - BUTTON_HEIGHT
    left_button_rect = pygame.Rect(panel_rect.x + PANEL_PADDING_X, buttons_y, button_width, BUTTON_HEIGHT)
    right_button_rect = pygame.Rect(left_button_rect.right + BUTTON_GAP, buttons_y, button_width, BUTTON_HEIGHT)

    return EventLayout(
        panel_rect,
        title_y,
        image_rect,
        description_rect,
        left_button_rect,
        right_button_rect,
        tab_rects,
    )


def _category_tab_rects(width: int, height: int) -> tuple[pygame.Rect, ...]:
    tab_width = max(130, min(170, int(width * 0.11)))
    tab_height = max(82, min(98, int(height * 0.12)))
    gap = max(20, int(width * 0.018))
    total_width = tab_width * len(CATEGORY_TABS) + gap * (len(CATEGORY_TABS) - 1)
    start_x = (width - total_width) // 2
    top = max(24, int(height * 0.035))
    return tuple(
        pygame.Rect(start_x + index * (tab_width + gap), top, tab_width, tab_height)
        for index in range(len(CATEGORY_TABS))
    )


def _draw_category_tabs(
    screen: pygame.Surface,
    tab_rects: tuple[pygame.Rect, ...],
    game_state=None,
) -> None:
    for index, ((stat, icon_name), rect) in enumerate(zip(CATEGORY_TABS, tab_rects)):
        visual_rect = rect

        _draw_tab_shadow(screen, visual_rect)
        tab_surface = pygame.Surface(visual_rect.size, pygame.SRCALPHA)
        pygame.draw.rect(tab_surface, (*PANEL_FILL, 226), tab_surface.get_rect(), border_radius=14)
        screen.blit(tab_surface, visual_rect)
        pygame.draw.rect(screen, MUTED_COBALT, visual_rect, 1, border_radius=14)
        pygame.draw.rect(screen, GOLD, visual_rect.inflate(-10, -10), 1, border_radius=10)

        icon_rect = pygame.Rect(0, 0, 52, 52)
        icon_rect.center = visual_rect.center
        _draw_category_icon(screen, icon_name, icon_rect, _category_fill_ratio(stat, game_state))

        if index < len(tab_rects) - 1:
            _draw_tab_separator(screen, visual_rect.right, visual_rect.centery)


def _draw_tab_shadow(screen: pygame.Surface, rect: pygame.Rect) -> None:
    shadow = pygame.Surface((rect.width + 18, rect.height + 18), pygame.SRCALPHA)
    pygame.draw.rect(shadow, (*PANEL_SHADOW, 42), shadow.get_rect(), border_radius=16)
    screen.blit(shadow, (rect.x - 5, rect.y + 7))


def _draw_category_icon(
    screen: pygame.Surface,
    icon_name: str,
    rect: pygame.Rect,
    fill_ratio: float,
) -> None:
    icon = _load_category_icon(icon_name)
    if not icon:
        return

    medallion = pygame.Surface((rect.width + 16, rect.height + 16), pygame.SRCALPHA)
    pygame.draw.ellipse(medallion, (*IVORY, 190), medallion.get_rect())
    pygame.draw.ellipse(medallion, (*GOLD_DARK, 150), medallion.get_rect(), 1)
    screen.blit(medallion, (rect.x - 8, rect.y - 8))

    sized_icon = pygame.transform.smoothscale(icon, rect.size)
    empty_icon = _icon_alpha_surface(sized_icon, MUTED_COBALT, 82)
    filled_icon = _icon_alpha_surface(sized_icon, COBALT, 255)
    screen.blit(empty_icon, rect)

    fill_height = int(rect.height * fill_ratio)
    if fill_height <= 0:
        return

    fill_area = pygame.Rect(0, rect.height - fill_height, rect.width, fill_height)
    screen.blit(filled_icon, (rect.x, rect.y + rect.height - fill_height), fill_area)


def _category_fill_ratio(label: str, game_state) -> float:
    if game_state is None:
        return 1.0

    value = game_state.stats.get(label, 100)
    return max(0.0, min(1.0, value / 100))


def _icon_alpha_surface(icon: pygame.Surface, color: tuple[int, int, int], alpha: int) -> pygame.Surface:
    mask = pygame.mask.from_surface(icon)
    return mask.to_surface(setcolor=(*color, alpha), unsetcolor=(0, 0, 0, 0))


def _draw_tab_separator(screen: pygame.Surface, x: int, y: int) -> None:
    pygame.draw.line(screen, (*GOLD_DARK, 170), (x + 10, y), (x + 28, y), 1)
    pygame.draw.circle(screen, GOLD, (x + 34, y), 3)
    pygame.draw.line(screen, (*GOLD_DARK, 170), (x + 40, y), (x + 58, y), 1)


def _draw_event_panel(screen: pygame.Surface, rect: pygame.Rect) -> None:
    shadow_surface = pygame.Surface((rect.width + 28, rect.height + 30), pygame.SRCALPHA)
    pygame.draw.rect(shadow_surface, (*PANEL_SHADOW, 70), shadow_surface.get_rect(), border_radius=PANEL_RADIUS + 3)
    screen.blit(shadow_surface, (rect.x - 10, rect.y + 10))

    panel = pygame.Surface(rect.size, pygame.SRCALPHA)
    pygame.draw.rect(panel, PANEL_FILL, panel.get_rect(), border_radius=PANEL_RADIUS)
    pygame.draw.rect(panel, COBALT, panel.get_rect(), PANEL_OUTER_BORDER_WIDTH, border_radius=PANEL_RADIUS)
    inner = panel.get_rect().inflate(-18, -18)
    pygame.draw.rect(panel, PANEL_INNER_FILL, inner, border_radius=PANEL_RADIUS - 7)
    pygame.draw.rect(panel, GOLD, inner, 2, border_radius=PANEL_RADIUS - 7)
    pygame.draw.rect(panel, (*COBALT, 150), panel.get_rect().inflate(-34, -34), 1, border_radius=PANEL_RADIUS - 11)
    _draw_panel_corners(panel, panel.get_rect())
    screen.blit(panel, rect)


def _draw_panel_corners(surface: pygame.Surface, rect: pygame.Rect) -> None:
    for x_sign in (-1, 1):
        for y_sign in (-1, 1):
            corner_x = rect.centerx + x_sign * (rect.width // 2 - 42)
            corner_y = rect.centery + y_sign * (rect.height // 2 - 42)
            pygame.draw.circle(surface, (*GOLD, 170), (corner_x, corner_y), 4)
            pygame.draw.circle(surface, (*COBALT, 130), (corner_x - x_sign * 18, corner_y), 3)
            pygame.draw.circle(surface, (*COBALT, 130), (corner_x, corner_y - y_sign * 18), 3)


def _draw_event_title(screen: pygame.Surface, title_text: str, panel_rect: pygame.Rect, title_y: int) -> None:
    title = config.FONT_EVENT_TITLE.render(title_text, True, COBALT)
    title_rect = title.get_rect(center=(panel_rect.centerx, title_y + title.get_height() // 2))
    screen.blit(title, title_rect)

    ornament_y = title_rect.bottom + 12
    left = panel_rect.centerx - 170
    right = panel_rect.centerx + 170
    pygame.draw.line(screen, GOLD_DARK, (left, ornament_y), (panel_rect.centerx - 22, ornament_y), 2)
    pygame.draw.line(screen, GOLD_DARK, (panel_rect.centerx + 22, ornament_y), (right, ornament_y), 2)
    pygame.draw.circle(screen, GOLD, (panel_rect.centerx, ornament_y), 6)
    pygame.draw.circle(screen, COBALT, (panel_rect.centerx, ornament_y), 2)


def _draw_event_image(
    screen: pygame.Surface,
    image_name: str | None,
    panel_rect: pygame.Rect,
    image_rect: pygame.Rect,
) -> None:
    if not image_name:
        frame_rect = image_rect.inflate(16, 16)
        _draw_image_frame(screen, frame_rect)
        _draw_missing_image_placeholder(screen, image_rect)
        return

    try:
        event_image = get_scaled_event_image(image_name, image_rect.width, image_rect.height)
    except (FileNotFoundError, pygame.error, ValueError) as exc:
        print(f"No se pudo cargar la imagen '{image_name}': {exc}")
        _draw_missing_image_placeholder(screen, image_rect)
        return

    image_rect = event_image.get_rect(center=image_rect.center)
    frame_rect = image_rect.inflate(16, 16)
    _draw_image_frame(screen, frame_rect)
    image_surface = _rounded_surface(event_image, IMAGE_RADIUS)
    image_position = image_surface.get_rect(center=image_rect.center)
    screen.blit(image_surface, image_position)


def _draw_event_description(screen: pygame.Surface, description: str, rect: pygame.Rect) -> None:
    draw_text_wrapped(screen, description, config.FONT_BODY_MEDIUM, INK, rect, line_spacing=0)


def _draw_image_frame(screen: pygame.Surface, frame_rect: pygame.Rect) -> None:
    pygame.draw.rect(screen, (*PANEL_SHADOW, 54), frame_rect.move(0, 7), border_radius=IMAGE_RADIUS + 4)
    pygame.draw.rect(screen, IVORY, frame_rect, border_radius=IMAGE_RADIUS + 4)
    pygame.draw.rect(screen, GOLD, frame_rect, 2, border_radius=IMAGE_RADIUS + 4)
    pygame.draw.rect(screen, COBALT, frame_rect.inflate(-8, -8), 1, border_radius=IMAGE_RADIUS)


def _draw_choice_buttons(screen: pygame.Surface, left_text: str, right_text: str, layout: EventLayout) -> None:
    mouse = pygame.mouse.get_pos()
    button_data = (
        (layout.left_button_rect, left_text, True),
        (layout.right_button_rect, right_text, False),
    )
    for index, (rect, text, is_primary) in enumerate(button_data):
        is_hovered = rect.collidepoint(mouse)
        target = 1.0 if is_hovered else 0.0
        _button_hover_progress[index] += (target - _button_hover_progress[index]) * BUTTON_HOVER_EASING
        _draw_choice_button(screen, rect, text, is_primary, _button_hover_progress[index])


def _draw_choice_button(
    screen: pygame.Surface,
    rect: pygame.Rect,
    text: str,
    is_primary: bool,
    hover_progress: float,
) -> None:
    lift = int(BUTTON_HOVER_LIFT * hover_progress)
    visual_rect = rect.move(0, -lift)
    shadow_alpha = int(62 + 45 * hover_progress)
    shadow = pygame.Surface((visual_rect.width + 18, visual_rect.height + 18), pygame.SRCALPHA)
    pygame.draw.rect(shadow, (*PANEL_SHADOW, shadow_alpha), shadow.get_rect(), border_radius=13)
    screen.blit(shadow, (visual_rect.x - 5, visual_rect.y + 8))

    fill = PRIMARY_BUTTON_FILL if is_primary else SECONDARY_BUTTON_FILL
    text_color = IVORY if is_primary else COBALT
    border_color = GOLD if is_primary else COBALT
    if hover_progress:
        fill = _blend_color(fill, GOLD if is_primary else IVORY, 0.1 * hover_progress)

    pygame.draw.rect(screen, fill, visual_rect, border_radius=11)
    pygame.draw.rect(screen, border_color, visual_rect, 2, border_radius=11)
    pygame.draw.rect(screen, GOLD, visual_rect.inflate(-10, -10), 1, border_radius=7)
    _draw_button_end_caps(screen, visual_rect, is_primary)

    text_rect = visual_rect.inflate(-32, -10)
    draw_text_wrapped(screen, text, config.FONT_BUTTON, text_color, text_rect, line_spacing=0)


def _draw_button_end_caps(screen: pygame.Surface, rect: pygame.Rect, is_primary: bool) -> None:
    accent = GOLD if is_primary else GOLD_DARK
    for x in (rect.x + 16, rect.right - 16):
        pygame.draw.circle(screen, accent, (x, rect.centery), 3)
        pygame.draw.line(screen, accent, (x - 7, rect.centery), (x + 7, rect.centery), 1)


def _draw_missing_image_placeholder(screen: pygame.Surface, rect: pygame.Rect) -> None:
    pygame.draw.rect(screen, (226, 220, 207), rect, border_radius=IMAGE_RADIUS)
    pygame.draw.rect(screen, COBALT, rect, 2, border_radius=IMAGE_RADIUS)


def _rounded_surface(surface: pygame.Surface, radius: int) -> pygame.Surface:
    rounded = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
    mask = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
    pygame.draw.rect(mask, (255, 255, 255, 255), mask.get_rect(), border_radius=radius)
    rounded.blit(surface, (0, 0))
    rounded.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
    return rounded


def _load_event_image(image_path: Path):
    if not image_path.exists():
        raise FileNotFoundError(image_path)

    return pygame.image.load(str(image_path)).convert_alpha()


def _load_category_icon(icon_name: str) -> pygame.Surface | None:
    if icon_name in _category_icon_cache:
        return _category_icon_cache[icon_name]

    icon_path = Path(config.ICON_PATH) / "categories" / icon_name
    try:
        _category_icon_cache[icon_name] = pygame.image.load(str(icon_path)).convert_alpha()
    except (FileNotFoundError, pygame.error) as exc:
        print(f"No se pudo cargar el icono de categoría '{icon_path}': {exc}")
        return None

    return _category_icon_cache[icon_name]


def _blend_color(base: tuple[int, int, int], target: tuple[int, int, int], ratio: float) -> tuple[int, int, int]:
    return tuple(int(base[index] + (target[index] - base[index]) * ratio) for index in range(3))


def _fit_line_with_suffix(line: str, font, max_width: int) -> str:
    suffix = TEXT_OVERFLOW_SUFFIX
    while line and font.size(line + suffix)[0] > max_width:
        line = line[:-1]

    return line.rstrip() + suffix
