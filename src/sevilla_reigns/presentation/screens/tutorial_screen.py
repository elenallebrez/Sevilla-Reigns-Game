import pygame

from sevilla_reigns.config import settings as config
from sevilla_reigns.presentation.screens import routes
from sevilla_reigns.presentation.ui.button import Button


SCREEN_FPS = 60
BACK_BUTTON_WIDTH = 200
BACK_BUTTON_HEIGHT = 50
TEXT_COLOR = (9, 45, 134)
PANEL_COLOR = (255, 252, 244, 225)
PANEL_BORDER_COLOR = (246, 205, 116)
PANEL_SHADOW_COLOR = (45, 35, 24)
MUTED_TEXT_COLOR = (87, 75, 64)
ACCENT_COLOR = config.ALBERO
ACCENT_DARK_COLOR = (176, 128, 44)
KEY_FILL_COLOR = (226, 220, 207)
KEY_BORDER_COLOR = config.BLUE_AZULEJO
STEP_BADGE_FILL = config.ALBERO
STEP_BADGE_TEXT = config.INK


def tutorial_screen(screen, WIDTH, HEIGHT, FONT, background_image):
    clock = pygame.time.Clock()
    running = True

    def go_back():
        nonlocal running
        running = False

    back_button = Button(
        "Volver",
        WIDTH // 2 - BACK_BUTTON_WIDTH // 2,
        int(HEIGHT * 0.78),
        BACK_BUTTON_WIDTH,
        BACK_BUTTON_HEIGHT,
        go_back,
        config.FONT_BUTTON,
    )

    tutorial_sections = [
        (
            "Lee la propuesta",
            "Cada carta presenta una decisión para Sevilla.",
        ),
        (
            "Elige una opción",
            "Puedes clicar una opción o usar el teclado.",
        ),
        (
            "Vigila tus indicadores",
            "Tradición, Vecindario, Dinero y Turismo cambian. Evita que lleguen al límite.",
        ),
    ]

    while running:
        screen.blit(background_image, (0, 0))

        panel_rect = pygame.Rect(int(WIDTH * 0.22), int(HEIGHT * 0.1), int(WIDTH * 0.56), int(HEIGHT * 0.64))
        _draw_panel(screen, panel_rect)
        _draw_tutorial_content(screen, panel_rect, FONT, tutorial_sections)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return routes.QUIT
            back_button.handle_event(event)

        back_button.draw(screen)
        pygame.display.flip()
        clock.tick(SCREEN_FPS)

    return routes.MENU


def _draw_panel(screen, rect):
    shadow = pygame.Surface((rect.width + 18, rect.height + 18), pygame.SRCALPHA)
    pygame.draw.rect(shadow, (*PANEL_SHADOW_COLOR, 75), shadow.get_rect(), border_radius=22)
    screen.blit(shadow, (rect.x + 7, rect.y + 10))

    panel = pygame.Surface(rect.size, pygame.SRCALPHA)
    pygame.draw.rect(panel, PANEL_COLOR, panel.get_rect(), border_radius=20)
    screen.blit(panel, rect)
    pygame.draw.rect(screen, TEXT_COLOR, rect, 4, border_radius=20)

    inner_rect = rect.inflate(-24, -24)
    pygame.draw.rect(screen, PANEL_BORDER_COLOR, inner_rect, 2, border_radius=14)
    pygame.draw.rect(screen, (*TEXT_COLOR, 145), rect.inflate(-44, -44), 1, border_radius=10)
    _draw_corner_ornaments(screen, inner_rect)


def _draw_corner_ornaments(screen, rect):
    for x in (rect.left + 20, rect.right - 20):
        for y in (rect.top + 20, rect.bottom - 20):
            pygame.draw.circle(screen, ACCENT_COLOR, (x, y), 4)
            pygame.draw.circle(screen, TEXT_COLOR, (x, y), 2)


def _draw_tutorial_content(screen, rect, font, sections):
    title = config.FONT_EVENT_TITLE.render("Cómo jugar", True, TEXT_COLOR)
    title_rect = title.get_rect(center=(rect.centerx, rect.top + int(rect.height * 0.12)))
    screen.blit(title, title_rect)
    _draw_separator(screen, rect.centerx, title_rect.bottom + 18, int(rect.width * 0.48))

    block_width = rect.width - 138
    block_height = 82
    block_gap = 12
    y = title_rect.bottom + 40
    for index, (heading, body) in enumerate(sections, start=1):
        block_rect = pygame.Rect(0, y, block_width, block_height)
        block_rect.centerx = rect.centerx
        _draw_tutorial_step(screen, block_rect, index, heading, body, config.FONT_SMALL, index == len(sections))
        y = block_rect.bottom + block_gap

        if index == 2:
            _draw_choice_controls(screen, rect.centerx, y - 4, config.FONT_SMALL)
            y += 52


def _draw_choice_controls(screen, center_x, y, font):
    left_text = "<- Opción izquierda"
    right_text = "Opción derecha ->"
    gap = 24
    left_surface = font.render(left_text, True, TEXT_COLOR)
    right_surface = font.render(right_text, True, TEXT_COLOR)
    control_width = max(left_surface.get_width(), right_surface.get_width()) + 34
    control_height = 38
    left_rect = pygame.Rect(center_x - gap // 2 - control_width, y, control_width, control_height)
    right_rect = pygame.Rect(center_x + gap // 2, y, control_width, control_height)

    for rect, surface in ((left_rect, left_surface), (right_rect, right_surface)):
        pygame.draw.rect(screen, KEY_FILL_COLOR, rect, border_radius=9)
        pygame.draw.rect(screen, KEY_BORDER_COLOR, rect, 2, border_radius=9)
        screen.blit(surface, surface.get_rect(center=rect.center))


def _draw_tutorial_step(screen, rect, number, heading, body, body_font, is_last=False):
    badge_radius = 17
    badge_center = (rect.left + badge_radius, rect.top + 22)
    pygame.draw.circle(screen, STEP_BADGE_FILL, badge_center, badge_radius)
    pygame.draw.circle(screen, TEXT_COLOR, badge_center, badge_radius, 2)

    number_surface = config.FONT_SMALL.render(str(number), True, STEP_BADGE_TEXT)
    screen.blit(number_surface, number_surface.get_rect(center=badge_center))

    heading_surface = config.FONT_SMALL.render(heading.upper(), True, MUTED_TEXT_COLOR)
    heading_rect = heading_surface.get_rect(topleft=(rect.left + 46, rect.top + 2))
    screen.blit(heading_surface, heading_rect)

    body_rect = pygame.Rect(rect.left + 46, heading_rect.bottom + 8, rect.width - 52, rect.height - 30)
    _draw_wrapped_text(screen, body, body_font, TEXT_COLOR, body_rect)
    if not is_last:
        _draw_subtle_separator(screen, rect.centerx, rect.bottom - 2, int(rect.width * 0.38))


def _draw_wrapped_text(screen, text, font, color, rect):
    words = text.split(" ")
    lines = []
    current_line = ""

    for word in words:
        test_line = f"{current_line} {word}".strip()
        if font.size(test_line)[0] <= rect.width:
            current_line = test_line
            continue

        if current_line:
            lines.append(current_line)
        current_line = word

    if current_line:
        lines.append(current_line)

    line_height = font.get_linesize() - 2
    max_lines = max(1, rect.height // line_height)
    if len(lines) > max_lines:
        lines = lines[:max_lines]

    y = rect.y
    for line in lines:
        surface = font.render(line, True, color)
        screen.blit(surface, (rect.left, y))
        y += line_height


def _draw_separator(screen, center_x, y, width):
    left = center_x - width // 2
    right = center_x + width // 2
    pygame.draw.line(screen, ACCENT_DARK_COLOR, (left, y), (right, y), 2)
    pygame.draw.circle(screen, ACCENT_COLOR, (center_x, y), 5)
    pygame.draw.circle(screen, TEXT_COLOR, (center_x, y), 2)


def _draw_subtle_separator(screen, center_x, y, width):
    left = center_x - width // 2
    right = center_x + width // 2
    pygame.draw.line(screen, (*ACCENT_DARK_COLOR, 150), (left, y), (right, y), 1)
