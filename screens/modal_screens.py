import os

import pygame

import config
from screens import routes


FINAL_OVERLAY_ALPHA = 150
FINAL_BOX_HORIZONTAL_MARGIN = 150
FINAL_BOX_HEIGHT = 200
FINAL_FADE_STEP = 5
FINAL_FADE_DELAY_MS = 30
FINAL_MUSIC_FADE_MS = 800
FINAL_BACKGROUND_COLOR = (30, 0, 0)
FINAL_BOX_COLOR = (80, 0, 0)
FINAL_BOX_BORDER_COLOR = (200, 0, 0)
FINAL_TEXT_COLOR = (255, 255, 255)
FINAL_INSTRUCTION_COLOR = (200, 200, 200)
FINAL_TITLE_Y_OFFSET = 30
FINAL_CAUSE_Y_OFFSET = 100
FINAL_INSTRUCTION_Y_OFFSET = 40
FINAL_BOX_BORDER_WIDTH = 4
FINAL_BOX_BORDER_RADIUS = 20
FINAL_MUSIC_VOLUME = 0.5

CONFIRM_BOX_WIDTH = 500
CONFIRM_BOX_HEIGHT = 200
CONFIRM_BUTTON_WIDTH = 120
CONFIRM_BUTTON_HEIGHT = 40
CONFIRM_BUTTON_SPACING = 40
CONFIRM_ANIMATION_SPEED = 20
CONFIRM_TEXT_Y_OFFSET = 30
CONFIRM_BUTTON_Y_OFFSET = 110
CONFIRM_BOX_COLOR = (255, 255, 255)
CONFIRM_BOX_BORDER_COLOR = (0, 0, 0)
CONFIRM_YES_COLOR = (200, 0, 0)
CONFIRM_NO_COLOR = (0, 150, 0)
CONFIRM_BOX_BORDER_WIDTH = 3
CONFIRM_BOX_BORDER_RADIUS = 15
CONFIRM_BUTTON_BORDER_RADIUS = 10

REELECTION_LINE_SPACING = 50
REELECTION_CONTINUE_FONT_SIZE = 30
REELECTION_CONTINUE_BOTTOM_MARGIN = 60
REELECTION_BACKGROUND_COLOR = config.CARD_IVORY
REELECTION_TEXT_COLOR = config.INK
REELECTION_CONTINUE_COLOR = config.BLUE_AZULEJO


def show_final_screen(screen, death_text: str, background_image: str | None):
    from core.sounds import reproducir_muerte, reproducir_musica

    width, height = screen.get_size()

    pygame.mixer.music.stop()
    reproducir_muerte()

    if background_image and os.path.exists(background_image):
        background = pygame.image.load(background_image).convert()
        background = pygame.transform.scale(background, (width, height))
        screen.blit(background, (0, 0))
    else:
        screen.fill(FINAL_BACKGROUND_COLOR)

    overlay = pygame.Surface((width, height))
    overlay.set_alpha(FINAL_OVERLAY_ALPHA)
    overlay.fill((0, 0, 0))
    screen.blit(overlay, (0, 0))

    box_width = width - FINAL_BOX_HORIZONTAL_MARGIN
    box_x = (width - box_width) // 2
    box_y = (height - FINAL_BOX_HEIGHT) // 2
    box_rect = pygame.Rect(box_x, box_y, box_width, FINAL_BOX_HEIGHT)

    pygame.draw.rect(screen, FINAL_BOX_COLOR, box_rect, border_radius=FINAL_BOX_BORDER_RADIUS)
    pygame.draw.rect(
        screen,
        FINAL_BOX_BORDER_COLOR,
        box_rect,
        FINAL_BOX_BORDER_WIDTH,
        border_radius=FINAL_BOX_BORDER_RADIUS,
    )

    title = config.BIG_FONT.render("Moción de censura", True, FINAL_TEXT_COLOR)
    cause = config.FONT.render(death_text, True, FINAL_TEXT_COLOR)
    instruction = config.FONT.render(
        "Pulsa cualquier botón para volver al menú",
        True,
        FINAL_INSTRUCTION_COLOR,
    )

    screen.blit(title, (width // 2 - title.get_width() // 2, box_y + FINAL_TITLE_Y_OFFSET))
    screen.blit(cause, (width // 2 - cause.get_width() // 2, box_y + FINAL_CAUSE_Y_OFFSET))
    screen.blit(
        instruction,
        (
            width // 2 - instruction.get_width() // 2,
            box_y + FINAL_BOX_HEIGHT + FINAL_INSTRUCTION_Y_OFFSET,
        ),
    )

    pygame.display.flip()
    result = _wait_for_continue()
    if result == routes.QUIT:
        return routes.QUIT

    _fade_to_black(screen, width, height)

    pygame.mixer.music.fadeout(FINAL_MUSIC_FADE_MS)
    reproducir_musica()
    pygame.mixer.music.set_volume(FINAL_MUSIC_VOLUME)
    pygame.mixer.music.play(-1, fade_ms=FINAL_MUSIC_FADE_MS)

    return routes.MENU


def show_exit_confirmation(screen):
    from core.sounds import click_sound

    local_clock = pygame.time.Clock()

    final_y = (config.HEIGHT - CONFIRM_BOX_HEIGHT) // 2
    box_x = (config.WIDTH - CONFIRM_BOX_WIDTH) // 2
    current_y = config.HEIGHT

    while True:
        screen_copy = screen.copy()

        overlay = pygame.Surface((config.WIDTH, config.HEIGHT))
        overlay.set_alpha(FINAL_OVERLAY_ALPHA)
        overlay.fill((0, 0, 0))
        screen.blit(screen_copy, (0, 0))
        screen.blit(overlay, (0, 0))

        current_y = max(final_y, current_y - CONFIRM_ANIMATION_SPEED)

        box_rect = pygame.Rect(box_x, current_y, CONFIRM_BOX_WIDTH, CONFIRM_BOX_HEIGHT)
        pygame.draw.rect(screen, CONFIRM_BOX_COLOR, box_rect, border_radius=CONFIRM_BOX_BORDER_RADIUS)
        pygame.draw.rect(
            screen,
            CONFIRM_BOX_BORDER_COLOR,
            box_rect,
            CONFIRM_BOX_BORDER_WIDTH,
            border_radius=CONFIRM_BOX_BORDER_RADIUS,
        )

        text = config.MEDIUM_FONT.render("¿Seguro que quieres salir?", True, config.BLACK)
        screen.blit(text, (box_x + (CONFIRM_BOX_WIDTH - text.get_width()) // 2, current_y + CONFIRM_TEXT_Y_OFFSET))

        yes_rect, no_rect = _confirmation_buttons(box_x, current_y)
        pygame.draw.rect(screen, CONFIRM_YES_COLOR, yes_rect, border_radius=CONFIRM_BUTTON_BORDER_RADIUS)
        pygame.draw.rect(screen, CONFIRM_NO_COLOR, no_rect, border_radius=CONFIRM_BUTTON_BORDER_RADIUS)

        yes_text = config.FONT.render("Sí", True, config.WHITE)
        no_text = config.FONT.render("No", True, config.WHITE)
        screen.blit(yes_text, yes_text.get_rect(center=yes_rect.center))
        screen.blit(no_text, no_text.get_rect(center=no_rect.center))

        pygame.display.flip()

        if current_y == final_y:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return routes.QUIT
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if yes_rect.collidepoint(event.pos):
                        click_sound.play()
                        return True
                    if no_rect.collidepoint(event.pos):
                        click_sound.play()
                        return False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_y:
                        return True
                    if event.key in (pygame.K_n, pygame.K_ESCAPE):
                        return False

        local_clock.tick(config.FPS)


def show_reelection_screen(screen, message: str = "Has sido reelegido"):
    screen.fill(REELECTION_BACKGROUND_COLOR)

    lines = message.split("\n")
    start_y = config.HEIGHT // 3

    for index, line in enumerate(lines):
        text = config.FONT.render(line, True, REELECTION_TEXT_COLOR)
        rect = text.get_rect(center=(config.WIDTH // 2, start_y + index * REELECTION_LINE_SPACING))
        screen.blit(text, rect)

    continue_text = pygame.font.Font(None, REELECTION_CONTINUE_FONT_SIZE).render(
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


def _confirmation_buttons(box_x: int, current_y: int) -> tuple[pygame.Rect, pygame.Rect]:
    yes_rect = pygame.Rect(
        box_x + (CONFIRM_BOX_WIDTH // 2 - CONFIRM_BUTTON_WIDTH - CONFIRM_BUTTON_SPACING // 2),
        current_y + CONFIRM_BUTTON_Y_OFFSET,
        CONFIRM_BUTTON_WIDTH,
        CONFIRM_BUTTON_HEIGHT,
    )
    no_rect = pygame.Rect(
        box_x + (CONFIRM_BOX_WIDTH // 2 + CONFIRM_BUTTON_SPACING // 2),
        current_y + CONFIRM_BUTTON_Y_OFFSET,
        CONFIRM_BUTTON_WIDTH,
        CONFIRM_BUTTON_HEIGHT,
    )
    return yes_rect, no_rect


def _wait_for_continue():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return routes.QUIT
            if event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                return None


def _fade_to_black(screen, width: int, height: int) -> None:
    fade_surface = pygame.Surface((width, height))
    fade_surface.fill((0, 0, 0))
    for alpha in range(0, 255, FINAL_FADE_STEP):
        fade_surface.set_alpha(alpha)
        screen.blit(fade_surface, (0, 0))
        pygame.display.flip()
        pygame.time.delay(FINAL_FADE_DELAY_MS)
