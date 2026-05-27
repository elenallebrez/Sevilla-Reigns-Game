import pygame

import config
from screens import routes
from ui.button import Button


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


def credits_screen(screen, WIDTH, HEIGHT, FONT, background_image):
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

    credits_sections = [
        ("Dirección, diseño y desarrollo", "Elena Fernández-Llebrez"),
        ("Arte, música y efectos", "Recursos generados y adaptados para esta versión"),
        ("Gracias por jugar a", "Tú Verás Lo Que Haces"),
    ]

    while running:
        screen.blit(background_image, (0, 0))

        panel_rect = pygame.Rect(int(WIDTH * 0.24), int(HEIGHT * 0.14), int(WIDTH * 0.52), int(HEIGHT * 0.57))
        _draw_panel(screen, panel_rect)
        _draw_credits_content(screen, panel_rect, FONT, credits_sections)

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


def _draw_credits_content(screen, rect, font, sections):
    title = config.FONT_EVENT_TITLE.render("Créditos", True, TEXT_COLOR)
    title_rect = title.get_rect(center=(rect.centerx, rect.top + int(rect.height * 0.16)))
    screen.blit(title, title_rect)
    _draw_separator(screen, rect.centerx, title_rect.bottom + 24, int(rect.width * 0.48))

    y = title_rect.bottom + 52
    max_text_width = rect.width - 92
    for label, value in sections:
        label_surface = _render_fitting_text(label, config.FONT_SMALL, MUTED_TEXT_COLOR, max_text_width)
        value_surface = _render_fitting_text(value, font, TEXT_COLOR, max_text_width)

        label_rect = label_surface.get_rect(center=(rect.centerx, y))
        value_rect = value_surface.get_rect(center=(rect.centerx, label_rect.bottom + 24))
        screen.blit(label_surface, label_rect)
        screen.blit(value_surface, value_rect)

        y = value_rect.bottom + 32


def _render_fitting_text(text, font, color, max_width):
    surface = font.render(text, True, color)
    if surface.get_width() <= max_width:
        return surface

    scale = max_width / surface.get_width()
    scaled_size = (max(1, int(surface.get_width() * scale)), max(1, int(surface.get_height() * scale)))
    return pygame.transform.smoothscale(surface, scaled_size)


def _draw_separator(screen, center_x, y, width):
    left = center_x - width // 2
    right = center_x + width // 2
    pygame.draw.line(screen, ACCENT_DARK_COLOR, (left, y), (right, y), 2)
    pygame.draw.circle(screen, ACCENT_COLOR, (center_x, y), 5)
    pygame.draw.circle(screen, TEXT_COLOR, (center_x, y), 2)
