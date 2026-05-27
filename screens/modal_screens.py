import os
import math

import pygame

import config
from screens import routes


FINAL_OVERLAY_ALPHA = 132
FINAL_BOX_WIDTH_RATIO = 0.58
FINAL_BOX_HEIGHT_RATIO = 0.46
FINAL_BOX_MIN_WIDTH = 640
FINAL_BOX_MAX_WIDTH = 880
FINAL_BOX_MIN_HEIGHT = 330
FINAL_BOX_MAX_HEIGHT = 430
FINAL_FADE_STEP = 5
FINAL_FADE_DELAY_MS = 30
FINAL_MUSIC_FADE_MS = 800
FINAL_BACKGROUND_COLOR = (38, 29, 23)
FINAL_OVERLAY_COLOR = (8, 10, 18)
FINAL_BOX_COLOR = config.CARD_IVORY
FINAL_BOX_INNER_COLOR = config.CAL_WHITE
FINAL_BOX_BORDER_COLOR = config.CLAVEL_RED
FINAL_BOX_ACCENT_COLOR = config.ALBERO
FINAL_TEXT_COLOR = config.INK
FINAL_MUTED_TEXT_COLOR = (98, 86, 75)
FINAL_INSTRUCTION_COLOR = config.BLUE_AZULEJO
FINAL_BOX_BORDER_WIDTH = 4
FINAL_BOX_BORDER_RADIUS = 22
FINAL_MUSIC_VOLUME = 0.5
FINAL_CLOCK_FPS = 60
FINAL_INSTRUCTION_PULSE_SPEED = 0.006
FINAL_INSTRUCTION_PULSE_AMOUNT = 0.055

CONFIRM_BOX_WIDTH_RATIO = 0.46
CONFIRM_BOX_HEIGHT_RATIO = 0.30
CONFIRM_BOX_MIN_WIDTH = 520
CONFIRM_BOX_MAX_WIDTH = 720
CONFIRM_BOX_MIN_HEIGHT = 240
CONFIRM_BOX_MAX_HEIGHT = 320
CONFIRM_BUTTON_WIDTH = 180
CONFIRM_BUTTON_HEIGHT = 50
CONFIRM_BUTTON_SPACING = 28
CONFIRM_ANIMATION_MS = 210
CONFIRM_OVERLAY_COLOR = (5, 12, 30)
CONFIRM_OVERLAY_ALPHA = 118
CONFIRM_BOX_COLOR = config.CARD_IVORY
CONFIRM_BOX_INNER_COLOR = config.CAL_WHITE
CONFIRM_BOX_BORDER_COLOR = config.BLUE_AZULEJO
CONFIRM_BOX_ACCENT_COLOR = config.ALBERO
CONFIRM_YES_COLOR = config.CLAVEL_RED
CONFIRM_YES_HOVER_COLOR = (188, 50, 54)
CONFIRM_YES_BORDER_COLOR = (92, 22, 24)
CONFIRM_CANCEL_COLOR = config.BLUE_AZULEJO
CONFIRM_CANCEL_HOVER_COLOR = (21, 64, 156)
CONFIRM_BOX_BORDER_WIDTH = 4
CONFIRM_BOX_BORDER_RADIUS = 22
CONFIRM_BUTTON_BORDER_RADIUS = 11
CONFIRM_BUTTON_HOVER_LIFT = 5
CONFIRM_BUTTON_HOVER_EASING = 0.22

REELECTION_LINE_SPACING = 50
REELECTION_CONTINUE_BOTTOM_MARGIN = 60
REELECTION_BACKGROUND_COLOR = config.CARD_IVORY
REELECTION_TEXT_COLOR = config.INK
REELECTION_CONTINUE_COLOR = config.BLUE_AZULEJO


def show_final_screen(screen, death_text: str, background_image: str | None):
    from core.sounds import reproducir_muerte, reproducir_musica

    width, height = screen.get_size()
    clock = pygame.time.Clock()

    pygame.mixer.music.stop()
    reproducir_muerte()

    background_scene = pygame.Surface((width, height))
    if background_image and os.path.exists(background_image):
        background = pygame.image.load(background_image).convert()
        background = pygame.transform.scale(background, (width, height))
        background_scene.blit(background, (0, 0))
    else:
        background_scene.fill(FINAL_BACKGROUND_COLOR)

    overlay = pygame.Surface((width, height))
    overlay.set_alpha(FINAL_OVERLAY_ALPHA)
    overlay.fill(FINAL_OVERLAY_COLOR)
    background_scene.blit(overlay, (0, 0))

    opened_at = pygame.time.get_ticks()
    result = _run_final_screen_loop(screen, background_scene, death_text, opened_at, clock)
    if result == routes.QUIT:
        return routes.QUIT

    _fade_to_black(screen, width, height)

    pygame.mixer.music.fadeout(FINAL_MUSIC_FADE_MS)
    reproducir_musica()
    pygame.mixer.music.set_volume(FINAL_MUSIC_VOLUME)
    pygame.mixer.music.play(-1, fade_ms=FINAL_MUSIC_FADE_MS)

    return routes.MENU


def _run_final_screen_loop(
    screen: pygame.Surface,
    background_scene: pygame.Surface,
    death_text: str,
    opened_at: int,
    clock: pygame.time.Clock,
):
    while True:
        now = pygame.time.get_ticks()
        screen.blit(background_scene, (0, 0))
        _draw_final_screen(screen, death_text, now - opened_at)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return routes.QUIT
            if event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                return None

        clock.tick(FINAL_CLOCK_FPS)


def _final_box_rect(screen: pygame.Surface) -> pygame.Rect:
    width, height = screen.get_size()
    box_width = max(FINAL_BOX_MIN_WIDTH, min(FINAL_BOX_MAX_WIDTH, int(width * FINAL_BOX_WIDTH_RATIO)))
    box_height = max(FINAL_BOX_MIN_HEIGHT, min(FINAL_BOX_MAX_HEIGHT, int(height * FINAL_BOX_HEIGHT_RATIO)))
    return pygame.Rect((width - box_width) // 2, (height - box_height) // 2 - 14, box_width, box_height)


def _draw_final_screen(screen: pygame.Surface, death_text: str, elapsed_ms: int) -> None:
    box_rect = _final_box_rect(screen)
    panel_surface = pygame.Surface((box_rect.width + 40, box_rect.height + 42), pygame.SRCALPHA)
    local_rect = pygame.Rect(20, 14, box_rect.width, box_rect.height)

    _draw_final_panel(panel_surface, local_rect)
    _draw_final_content(panel_surface, local_rect, death_text)
    screen.blit(panel_surface, (box_rect.x - 20, box_rect.y - 14))
    _draw_final_continue_prompt(screen, box_rect, elapsed_ms)


def _draw_final_panel(surface: pygame.Surface, rect: pygame.Rect) -> None:
    shadow = pygame.Surface((rect.width + 38, rect.height + 42), pygame.SRCALPHA)
    pygame.draw.rect(shadow, (*config.TILE_SHADOW, 105), shadow.get_rect(), border_radius=FINAL_BOX_BORDER_RADIUS + 5)
    surface.blit(shadow, (-14, 13))

    pygame.draw.rect(surface, FINAL_BOX_COLOR, rect, border_radius=FINAL_BOX_BORDER_RADIUS)
    pygame.draw.rect(
        surface,
        FINAL_BOX_BORDER_COLOR,
        rect,
        FINAL_BOX_BORDER_WIDTH,
        border_radius=FINAL_BOX_BORDER_RADIUS,
    )
    inner_rect = rect.inflate(-22, -22)
    pygame.draw.rect(surface, FINAL_BOX_INNER_COLOR, inner_rect, border_radius=FINAL_BOX_BORDER_RADIUS - 8)
    pygame.draw.rect(surface, FINAL_BOX_ACCENT_COLOR, inner_rect, 2, border_radius=FINAL_BOX_BORDER_RADIUS - 8)
    pygame.draw.rect(surface, (*config.BLUE_AZULEJO, 145), rect.inflate(-42, -42), 1, border_radius=10)
    _draw_final_ornaments(surface, rect)


def _draw_final_ornaments(surface: pygame.Surface, rect: pygame.Rect) -> None:
    ornament_y = rect.y + 92
    center_x = rect.centerx
    pygame.draw.line(surface, FINAL_BOX_ACCENT_COLOR, (center_x - 178, ornament_y), (center_x - 25, ornament_y), 2)
    pygame.draw.line(surface, FINAL_BOX_ACCENT_COLOR, (center_x + 25, ornament_y), (center_x + 178, ornament_y), 2)
    pygame.draw.circle(surface, FINAL_BOX_ACCENT_COLOR, (center_x, ornament_y), 6)
    pygame.draw.circle(surface, FINAL_BOX_BORDER_COLOR, (center_x, ornament_y), 2)

    for x_sign in (-1, 1):
        for y_sign in (-1, 1):
            corner = (
                rect.centerx + x_sign * (rect.width // 2 - 44),
                rect.centery + y_sign * (rect.height // 2 - 44),
            )
            pygame.draw.circle(surface, (*FINAL_BOX_ACCENT_COLOR, 180), corner, 4)
            pygame.draw.circle(surface, (*config.BLUE_AZULEJO, 135), (corner[0] - x_sign * 18, corner[1]), 3)
            pygame.draw.circle(surface, (*config.BLUE_AZULEJO, 135), (corner[0], corner[1] - y_sign * 18), 3)


def _draw_final_content(surface: pygame.Surface, rect: pygame.Rect, death_text: str) -> None:
    title = config.FONT_EVENT_TITLE.render("Moción de censura", True, FINAL_BOX_BORDER_COLOR)
    title_rect = title.get_rect(center=(rect.centerx, rect.y + 58))
    surface.blit(title, title_rect)

    cause_rect = pygame.Rect(rect.x + 72, rect.y + 128, rect.width - 144, rect.height - 188)
    _draw_wrapped_centered_text(surface, death_text, config.FONT_BODY_MEDIUM, FINAL_TEXT_COLOR, cause_rect, 8)

    footer = config.FONT_SMALL.render("Tu mandato termina aquí.", True, FINAL_MUTED_TEXT_COLOR)
    surface.blit(footer, footer.get_rect(center=(rect.centerx, rect.bottom - 48)))


def _draw_final_continue_prompt(screen: pygame.Surface, box_rect: pygame.Rect, elapsed_ms: int) -> None:
    prompt = config.FONT_SMALL.render("Pulsa cualquier botón para volver al menú", True, FINAL_INSTRUCTION_COLOR)
    pulse = 1 + FINAL_INSTRUCTION_PULSE_AMOUNT * math.sin(elapsed_ms * FINAL_INSTRUCTION_PULSE_SPEED)
    scaled_size = (
        max(1, int(prompt.get_width() * pulse)),
        max(1, int(prompt.get_height() * pulse)),
    )
    prompt = pygame.transform.smoothscale(prompt, scaled_size)
    prompt_rect = prompt.get_rect(center=(box_rect.centerx, box_rect.bottom + 48))

    pill_rect = prompt_rect.inflate(44, 20)
    pill = pygame.Surface(pill_rect.size, pygame.SRCALPHA)
    pygame.draw.rect(pill, (*config.CAL_WHITE, 216), pill.get_rect(), border_radius=14)
    pygame.draw.rect(pill, (*FINAL_BOX_ACCENT_COLOR, 185), pill.get_rect(), 2, border_radius=14)
    screen.blit(pill, pill_rect)
    screen.blit(prompt, prompt_rect)


def _draw_wrapped_centered_text(
    surface: pygame.Surface,
    text: str,
    font: pygame.font.Font,
    color: tuple[int, int, int],
    rect: pygame.Rect,
    line_spacing: int,
) -> None:
    words = text.split()
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

    line_height = font.get_linesize() + line_spacing
    max_lines = max(1, rect.height // line_height)
    if len(lines) > max_lines:
        lines = lines[:max_lines]
        lines[-1] = _fit_text_with_suffix(lines[-1], font, rect.width)

    total_height = len(lines) * font.get_linesize() + max(0, len(lines) - 1) * line_spacing
    y = rect.y + max(0, (rect.height - total_height) // 2)
    for line in lines:
        rendered = font.render(line, True, color)
        surface.blit(rendered, rendered.get_rect(center=(rect.centerx, y + rendered.get_height() // 2)))
        y += font.get_linesize() + line_spacing


def _fit_text_with_suffix(text: str, font: pygame.font.Font, max_width: int) -> str:
    suffix = "..."
    while text and font.size(text + suffix)[0] > max_width:
        text = text[:-1]
    return text.rstrip() + suffix


def show_exit_confirmation(screen):
    from core.sounds import click_sound

    local_clock = pygame.time.Clock()
    return _show_exit_confirmation_polished(screen, local_clock, click_sound)


def show_reelection_screen(screen, message: str = "Has sido reelegido"):
    screen.fill(REELECTION_BACKGROUND_COLOR)

    lines = message.split("\n")
    start_y = config.HEIGHT // 3

    for index, line in enumerate(lines):
        text = config.FONT_BODY_MEDIUM.render(line, True, REELECTION_TEXT_COLOR)
        rect = text.get_rect(center=(config.WIDTH // 2, start_y + index * REELECTION_LINE_SPACING))
        screen.blit(text, rect)

    continue_text = config.FONT_SMALL.render(
        "Presiona cualquier tecla para continuar...",
        True,
        REELECTION_CONTINUE_COLOR,
    )
    continue_rect = continue_text.get_rect(
        center=(config.WIDTH // 2, config.HEIGHT - REELECTION_CONTINUE_BOTTOM_MARGIN)
    )
    screen.blit(continue_text, continue_rect)

    pygame.display.flip()

    waiting = True
    while waiting:
        config.clock.tick(config.FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return routes.QUIT
            if event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                waiting = False

    return None


def _show_exit_confirmation_polished(screen, local_clock, click_sound):
    frozen_scene = screen.copy()
    opened_at = pygame.time.get_ticks()
    hover_progress = {"yes": 0.0, "cancel": 0.0}

    while True:
        progress = min(1.0, (pygame.time.get_ticks() - opened_at) / CONFIRM_ANIMATION_MS)
        box_rect = _exit_confirmation_box_rect(screen)
        yes_rect, cancel_rect = _exit_confirmation_buttons(box_rect)

        screen.blit(frozen_scene, (0, 0))
        _draw_exit_confirmation_overlay(screen, progress)
        _update_exit_confirmation_hover(hover_progress, yes_rect, cancel_rect)
        _draw_exit_confirmation_modal(screen, box_rect, yes_rect, cancel_rect, hover_progress, progress)

        pygame.display.flip()

        if progress >= 1.0:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return routes.QUIT
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if yes_rect.collidepoint(event.pos):
                        click_sound.play()
                        return True
                    if cancel_rect.collidepoint(event.pos):
                        click_sound.play()
                        return False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_y:
                        return True
                    if event.key in (pygame.K_n, pygame.K_ESCAPE):
                        return False

        local_clock.tick(config.FPS)


def _exit_confirmation_box_rect(screen) -> pygame.Rect:
    width, height = screen.get_size()
    box_width = max(CONFIRM_BOX_MIN_WIDTH, min(CONFIRM_BOX_MAX_WIDTH, int(width * CONFIRM_BOX_WIDTH_RATIO)))
    box_height = max(CONFIRM_BOX_MIN_HEIGHT, min(CONFIRM_BOX_MAX_HEIGHT, int(height * CONFIRM_BOX_HEIGHT_RATIO)))
    return pygame.Rect((width - box_width) // 2, (height - box_height) // 2, box_width, box_height)


def _exit_confirmation_buttons(box_rect: pygame.Rect) -> tuple[pygame.Rect, pygame.Rect]:
    total_width = CONFIRM_BUTTON_WIDTH * 2 + CONFIRM_BUTTON_SPACING
    start_x = box_rect.centerx - total_width // 2
    button_y = box_rect.bottom - 82
    yes_rect = pygame.Rect(start_x, button_y, CONFIRM_BUTTON_WIDTH, CONFIRM_BUTTON_HEIGHT)
    cancel_rect = pygame.Rect(
        yes_rect.right + CONFIRM_BUTTON_SPACING,
        button_y,
        CONFIRM_BUTTON_WIDTH,
        CONFIRM_BUTTON_HEIGHT,
    )
    return yes_rect, cancel_rect


def _draw_exit_confirmation_overlay(screen, progress: float) -> None:
    overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
    overlay.fill((*CONFIRM_OVERLAY_COLOR, int(CONFIRM_OVERLAY_ALPHA * progress)))
    screen.blit(overlay, (0, 0))


def _update_exit_confirmation_hover(
    hover_progress: dict[str, float],
    yes_rect: pygame.Rect,
    cancel_rect: pygame.Rect,
) -> None:
    mouse = pygame.mouse.get_pos()
    targets = {
        "yes": 1.0 if yes_rect.collidepoint(mouse) else 0.0,
        "cancel": 1.0 if cancel_rect.collidepoint(mouse) else 0.0,
    }
    for key, target in targets.items():
        hover_progress[key] += (target - hover_progress[key]) * CONFIRM_BUTTON_HOVER_EASING


def _draw_exit_confirmation_modal(
    screen,
    box_rect: pygame.Rect,
    yes_rect: pygame.Rect,
    cancel_rect: pygame.Rect,
    hover_progress: dict[str, float],
    progress: float,
) -> None:
    modal_surface = pygame.Surface(box_rect.size, pygame.SRCALPHA)
    surface_rect = modal_surface.get_rect()

    _draw_exit_confirmation_panel(modal_surface, surface_rect)
    _draw_exit_confirmation_text(modal_surface, surface_rect)

    _draw_exit_confirmation_button(
        modal_surface,
        yes_rect.move(-box_rect.x, -box_rect.y),
        "Sí, salir",
        CONFIRM_YES_COLOR,
        CONFIRM_YES_HOVER_COLOR,
        CONFIRM_YES_BORDER_COLOR,
        config.CAL_WHITE,
        hover_progress["yes"],
    )
    _draw_exit_confirmation_button(
        modal_surface,
        cancel_rect.move(-box_rect.x, -box_rect.y),
        "Cancelar",
        CONFIRM_CANCEL_COLOR,
        CONFIRM_CANCEL_HOVER_COLOR,
        CONFIRM_BOX_ACCENT_COLOR,
        config.CAL_WHITE,
        hover_progress["cancel"],
    )

    scale = 0.96 + 0.04 * _ease_out_cubic(progress)
    if scale < 1:
        scaled_size = (max(1, int(box_rect.width * scale)), max(1, int(box_rect.height * scale)))
        modal_surface = pygame.transform.smoothscale(modal_surface, scaled_size)

    modal_surface.set_alpha(int(255 * progress))
    screen.blit(modal_surface, modal_surface.get_rect(center=box_rect.center))


def _draw_exit_confirmation_panel(surface: pygame.Surface, rect: pygame.Rect) -> None:
    shadow = pygame.Surface((rect.width + 36, rect.height + 38), pygame.SRCALPHA)
    pygame.draw.rect(shadow, (*config.TILE_SHADOW, 100), shadow.get_rect(), border_radius=CONFIRM_BOX_BORDER_RADIUS + 5)
    surface.blit(shadow, (-14, 13))

    pygame.draw.rect(surface, CONFIRM_BOX_COLOR, rect, border_radius=CONFIRM_BOX_BORDER_RADIUS)
    pygame.draw.rect(
        surface,
        CONFIRM_BOX_BORDER_COLOR,
        rect,
        CONFIRM_BOX_BORDER_WIDTH,
        border_radius=CONFIRM_BOX_BORDER_RADIUS,
    )
    inner_rect = rect.inflate(-22, -22)
    pygame.draw.rect(surface, CONFIRM_BOX_INNER_COLOR, inner_rect, border_radius=CONFIRM_BOX_BORDER_RADIUS - 8)
    pygame.draw.rect(surface, CONFIRM_BOX_ACCENT_COLOR, inner_rect, 2, border_radius=CONFIRM_BOX_BORDER_RADIUS - 8)
    pygame.draw.rect(surface, (*CONFIRM_BOX_BORDER_COLOR, 150), rect.inflate(-42, -42), 1, border_radius=10)
    _draw_exit_confirmation_ornaments(surface, rect)


def _draw_exit_confirmation_ornaments(surface: pygame.Surface, rect: pygame.Rect) -> None:
    ornament_y = rect.y + 86
    center_x = rect.centerx
    pygame.draw.line(surface, CONFIRM_BOX_ACCENT_COLOR, (center_x - 160, ornament_y), (center_x - 22, ornament_y), 2)
    pygame.draw.line(surface, CONFIRM_BOX_ACCENT_COLOR, (center_x + 22, ornament_y), (center_x + 160, ornament_y), 2)
    pygame.draw.circle(surface, CONFIRM_BOX_ACCENT_COLOR, (center_x, ornament_y), 6)
    pygame.draw.circle(surface, CONFIRM_BOX_BORDER_COLOR, (center_x, ornament_y), 2)

    for x_sign in (-1, 1):
        for y_sign in (-1, 1):
            corner = (
                rect.centerx + x_sign * (rect.width // 2 - 42),
                rect.centery + y_sign * (rect.height // 2 - 42),
            )
            pygame.draw.circle(surface, (*CONFIRM_BOX_ACCENT_COLOR, 180), corner, 4)
            pygame.draw.circle(surface, (*CONFIRM_BOX_BORDER_COLOR, 145), (corner[0] - x_sign * 17, corner[1]), 3)
            pygame.draw.circle(surface, (*CONFIRM_BOX_BORDER_COLOR, 145), (corner[0], corner[1] - y_sign * 17), 3)


def _draw_exit_confirmation_text(surface: pygame.Surface, rect: pygame.Rect) -> None:
    title = config.FONT_EVENT_TITLE.render("¿Quieres salir del juego?", True, CONFIRM_BOX_BORDER_COLOR)
    surface.blit(title, title.get_rect(center=(rect.centerx, rect.y + 58)))


def _draw_exit_confirmation_button(
    surface: pygame.Surface,
    rect: pygame.Rect,
    label: str,
    fill: tuple[int, int, int],
    hover_fill: tuple[int, int, int],
    border: tuple[int, int, int],
    text_color: tuple[int, int, int],
    hover_progress: float,
) -> None:
    visual_rect = rect.move(0, -int(CONFIRM_BUTTON_HOVER_LIFT * hover_progress))
    shadow_alpha = int(70 + 55 * hover_progress)
    shadow = pygame.Surface((visual_rect.width + 18, visual_rect.height + 18), pygame.SRCALPHA)
    pygame.draw.rect(shadow, (*config.TILE_SHADOW, shadow_alpha), shadow.get_rect(), border_radius=14)
    surface.blit(shadow, (visual_rect.x - 5, visual_rect.y + 8))

    pygame.draw.rect(surface, _blend_color(fill, hover_fill, hover_progress), visual_rect, border_radius=CONFIRM_BUTTON_BORDER_RADIUS)
    pygame.draw.rect(surface, border, visual_rect, 2, border_radius=CONFIRM_BUTTON_BORDER_RADIUS)
    pygame.draw.rect(surface, CONFIRM_BOX_ACCENT_COLOR, visual_rect.inflate(-10, -10), 1, border_radius=7)

    text = config.FONT_BUTTON.render(label, True, text_color)
    surface.blit(text, text.get_rect(center=visual_rect.center))


def _blend_color(base: tuple[int, int, int], target: tuple[int, int, int], ratio: float) -> tuple[int, int, int]:
    return tuple(int(base[index] + (target[index] - base[index]) * ratio) for index in range(3))


def _ease_out_cubic(progress: float) -> float:
    return 1 - pow(1 - progress, 3)


def _fade_to_black(screen, width: int, height: int) -> None:
    fade_surface = pygame.Surface((width, height))
    fade_surface.fill((0, 0, 0))
    for alpha in range(0, 255, FINAL_FADE_STEP):
        fade_surface.set_alpha(alpha)
        screen.blit(fade_surface, (0, 0))
        pygame.display.flip()
        pygame.time.delay(FINAL_FADE_DELAY_MS)
