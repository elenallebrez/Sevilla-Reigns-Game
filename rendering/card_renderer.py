from pathlib import Path

import pygame

import config


STATS_AREA_HEIGHT = 142
CARD_HORIZONTAL_MARGIN = 160
CARD_BOTTOM_PADDING = 32
CARD_BORDER_WIDTH = 4
CARD_TITLE_TOP_PADDING = 28
CARD_CONTENT_GAP = 18
CARD_IMAGE_MAX_WIDTH_RATIO = 0.8
CARD_RESERVED_BOTTOM_SPACE = 140
CARD_TEXT_HORIZONTAL_PADDING = 56
CARD_DESCRIPTION_HEIGHT = 96
CARD_OPTIONS_BOTTOM_PADDING = 64
CARD_RADIUS = 18
OPTION_HEIGHT = 54
OPTION_GAP = 30
TEXT_LINE_SPACING = 5
TEXT_OVERFLOW_SUFFIX = "..."
FALLBACK_IMAGE_COLOR = (226, 220, 207)
FALLBACK_IMAGE_BORDER_COLOR = config.BLUE_AZULEJO
CARD_SHADOW_COLOR = (75, 58, 38)
CARD_BORDER_COLOR = config.BLUE_AZULEJO
CARD_INNER_BORDER_COLOR = config.ALBERO
CARD_TITLE_COLOR = config.INK
CARD_TEXT_COLOR = config.INK
OPTION_FILL_COLOR = (*config.CAL_WHITE, 235)
OPTION_BORDER_COLOR = config.ALBERO

_event_image_cache = {}
_scaled_event_image_cache = {}


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
    new_size = (int(original_width * scale), int(original_height * scale))
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

    y = rect.y
    line_height = font.get_linesize() + line_spacing
    max_lines = max(1, rect.height // line_height)

    if len(lines) > max_lines:
        lines = lines[:max_lines]
        lines[-1] = _fit_line_with_suffix(lines[-1], font, rect.width)

    for line in lines:
        rendered_text = font.render(line, True, color)
        surface.blit(rendered_text, (rect.x + (rect.width - rendered_text.get_width()) // 2, y))
        y += rendered_text.get_height() + line_spacing

    return y - rect.y


def draw_event(screen, event, swipe_offset: int) -> None:
    width = screen.get_width()
    height = screen.get_height()

    card_width = min(width - 96, 1160)
    card_height = height - STATS_AREA_HEIGHT - CARD_BOTTOM_PADDING
    card_x = (width - card_width) // 2
    card_y = STATS_AREA_HEIGHT

    card_rect = pygame.Rect(card_x + swipe_offset, card_y, card_width, card_height)
    shadow_rect = card_rect.move(8, 10)
    pygame.draw.rect(screen, CARD_SHADOW_COLOR, shadow_rect, border_radius=CARD_RADIUS)
    pygame.draw.rect(screen, config.CARD_IVORY, card_rect, border_radius=CARD_RADIUS)
    pygame.draw.rect(screen, CARD_BORDER_COLOR, card_rect, CARD_BORDER_WIDTH, border_radius=CARD_RADIUS)

    inner_rect = card_rect.inflate(-18, -18)
    pygame.draw.rect(screen, CARD_INNER_BORDER_COLOR, inner_rect, 2, border_radius=CARD_RADIUS - 6)
    _draw_ornamental_lines(screen, inner_rect)

    title = config.BIG_FONT.render(event.title, True, CARD_TITLE_COLOR)
    title_y = card_y + CARD_TITLE_TOP_PADDING
    screen.blit(title, (card_rect.centerx - title.get_width() // 2, title_y))

    image_height = int(card_height * 0.6)
    image_y = title_y + title.get_height() + CARD_CONTENT_GAP

    if event.image:
        free_space = card_rect.bottom - CARD_RESERVED_BOTTOM_SPACE - image_y
        max_width = int(card_width * CARD_IMAGE_MAX_WIDTH_RATIO)
        image_height = _draw_event_image(screen, event.image, card_rect, image_y, max_width, free_space)

    desc_y = image_y + image_height + CARD_CONTENT_GAP
    desc_rect = pygame.Rect(
        card_rect.left + CARD_TEXT_HORIZONTAL_PADDING,
        desc_y,
        card_width - CARD_TEXT_HORIZONTAL_PADDING * 2,
        CARD_DESCRIPTION_HEIGHT,
    )
    draw_text_wrapped(screen, event.description, config.FONT, CARD_TEXT_COLOR, desc_rect)

    options_y = card_rect.bottom - CARD_OPTIONS_BOTTOM_PADDING
    option_width = (card_width - CARD_TEXT_HORIZONTAL_PADDING * 2 - OPTION_GAP) // 2
    left_rect = pygame.Rect(card_rect.left + CARD_TEXT_HORIZONTAL_PADDING, options_y - 10, option_width, OPTION_HEIGHT)
    right_rect = pygame.Rect(left_rect.right + OPTION_GAP, options_y - 10, option_width, OPTION_HEIGHT)
    _draw_option(screen, left_rect, event.options[0].text)
    _draw_option(screen, right_rect, event.options[1].text)


def _draw_event_image(screen, image_name: str, card_rect, image_y: int, max_width: int, max_height: int) -> int:
    try:
        event_image = get_scaled_event_image(image_name, max_width, max_height)
    except (FileNotFoundError, pygame.error, ValueError) as exc:
        print(f"No se pudo cargar la imagen '{image_name}': {exc}")
        return _draw_missing_image_placeholder(screen, card_rect, image_y, max_width, max_height)

    image_width, image_height = event_image.get_size()
    image_x = card_rect.centerx - image_width // 2
    screen.blit(event_image, (image_x, image_y))
    return image_height


def _load_event_image(image_path: Path):
    if not image_path.exists():
        raise FileNotFoundError(image_path)

    return pygame.image.load(str(image_path)).convert_alpha()


def _draw_missing_image_placeholder(screen, card_rect, image_y: int, max_width: int, max_height: int) -> int:
    fallback_width = max(1, max_width)
    fallback_height = max(1, min(max_height, int(max_width * 0.6)))
    fallback_rect = pygame.Rect(
        card_rect.centerx - fallback_width // 2,
        image_y,
        fallback_width,
        fallback_height,
    )
    pygame.draw.rect(screen, FALLBACK_IMAGE_COLOR, fallback_rect)
    pygame.draw.rect(screen, FALLBACK_IMAGE_BORDER_COLOR, fallback_rect, 2)
    return fallback_height


def _draw_ornamental_lines(screen, rect) -> None:
    left = rect.left + 28
    right = rect.right - 28
    pygame.draw.line(screen, CARD_BORDER_COLOR, (left, rect.top + 24), (right, rect.top + 24), 2)
    pygame.draw.line(screen, CARD_BORDER_COLOR, (left, rect.bottom - 76), (right, rect.bottom - 76), 2)
    pygame.draw.circle(screen, config.CLAVEL_RED, (left, rect.top + 24), 5)
    pygame.draw.circle(screen, config.CLAVEL_RED, (right, rect.top + 24), 5)
    pygame.draw.circle(screen, config.CLAVEL_RED, (left, rect.bottom - 76), 5)
    pygame.draw.circle(screen, config.CLAVEL_RED, (right, rect.bottom - 76), 5)


def _draw_option(screen, rect, text: str) -> None:
    option_surface = pygame.Surface(rect.size, pygame.SRCALPHA)
    pygame.draw.rect(option_surface, OPTION_FILL_COLOR, option_surface.get_rect(), border_radius=10)
    screen.blit(option_surface, rect)
    pygame.draw.rect(screen, OPTION_BORDER_COLOR, rect, 2, border_radius=10)

    text_rect = rect.inflate(-20, -8)
    draw_text_wrapped(screen, text, config.FONT, CARD_TEXT_COLOR, text_rect, line_spacing=0)


def _fit_line_with_suffix(line: str, font, max_width: int) -> str:
    suffix = TEXT_OVERFLOW_SUFFIX
    while line and font.size(line + suffix)[0] > max_width:
        line = line[:-1]

    return line.rstrip() + suffix
