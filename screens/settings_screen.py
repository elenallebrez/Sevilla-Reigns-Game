import pygame

import config
from core.sounds import cambiar_volumen, cambiar_volumen_sonidos, click_sound
from screens import routes
from ui.button import Button


SCREEN_FPS = 60
DEFAULT_VOLUME = 0.5
SLIDER_WIDTH_RATIO = 0.28
SLIDER_HEIGHT = 26
BACK_BUTTON_WIDTH = 200
BACK_BUTTON_HEIGHT = 50
TEXT_COLOR = (9, 45, 134)
SLIDER_BACKGROUND_COLOR = (226, 220, 207)
SLIDER_FILL_COLOR = config.OLIVE_GREEN
SLIDER_BORDER_COLOR = config.BLUE_AZULEJO
SLIDER_THUMB_COLOR = config.ALBERO
SLIDER_THUMB_RADIUS = 15
PANEL_COLOR = (255, 252, 244, 225)


def settings_screen(screen, WIDTH, HEIGHT, FONT, background_image, settings_state):
    clock = pygame.time.Clock()
    running = True

    volumen_musica = settings_state.music_volume
    volumen_sonidos = settings_state.sound_volume
    cambiar_volumen(volumen_musica)
    cambiar_volumen_sonidos(volumen_sonidos)
    active_slider = None

    slider_width = max(260, int(WIDTH * SLIDER_WIDTH_RATIO))
    barra_musica_rect = pygame.Rect(WIDTH // 2 - slider_width // 2, int(HEIGHT * 0.42), slider_width, SLIDER_HEIGHT)
    barra_sonidos_rect = pygame.Rect(WIDTH // 2 - slider_width // 2, int(HEIGHT * 0.54), slider_width, SLIDER_HEIGHT)

    def set_music_volume(mouse_x):
        nonlocal volumen_musica
        volumen_musica = _value_from_slider_x(barra_musica_rect, mouse_x)
        settings_state.music_volume = volumen_musica
        cambiar_volumen(volumen_musica)

    def set_sound_volume(mouse_x):
        nonlocal volumen_sonidos
        volumen_sonidos = _value_from_slider_x(barra_sonidos_rect, mouse_x)
        settings_state.sound_volume = volumen_sonidos
        cambiar_volumen_sonidos(volumen_sonidos)

    def go_back():
        nonlocal running
        click_sound.play()
        running = False

    volver_btn = Button(
        "Volver",
        WIDTH // 2 - BACK_BUTTON_WIDTH // 2,
        int(HEIGHT * 0.78),
        BACK_BUTTON_WIDTH,
        BACK_BUTTON_HEIGHT,
        go_back,
        config.FONT_BUTTON,
    )

    while running:
        screen.blit(background_image, (0, 0))

        panel_rect = pygame.Rect(int(WIDTH * 0.28), int(HEIGHT * 0.18), int(WIDTH * 0.44), int(HEIGHT * 0.5))
        panel = pygame.Surface(panel_rect.size, pygame.SRCALPHA)
        pygame.draw.rect(panel, PANEL_COLOR, panel.get_rect(), border_radius=18)
        screen.blit(panel, panel_rect)
        pygame.draw.rect(screen, config.ALBERO, panel_rect, 3, border_radius=18)

        titulo = config.FONT_EVENT_TITLE.render("Ajustes", True, TEXT_COLOR)
        screen.blit(titulo, (WIDTH // 2 - titulo.get_width() // 2, int(HEIGHT * 0.24)))

        texto_musica = FONT.render("Volumen música", True, TEXT_COLOR)
        screen.blit(
            texto_musica,
            (WIDTH // 2 - texto_musica.get_width() // 2, barra_musica_rect.y - 40),
        )

        texto_sonidos = FONT.render("Volumen efectos", True, TEXT_COLOR)
        screen.blit(
            texto_sonidos,
            (WIDTH // 2 - texto_sonidos.get_width() // 2, barra_sonidos_rect.y - 40),
        )

        _draw_slider(screen, barra_musica_rect, volumen_musica, FONT)
        _draw_slider(screen, barra_sonidos_rect, volumen_sonidos, FONT)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return routes.QUIT

            if event.type == pygame.MOUSEBUTTONDOWN:
                music_thumb_rect = _thumb_hit_rect(barra_musica_rect, volumen_musica)
                sound_thumb_rect = _thumb_hit_rect(barra_sonidos_rect, volumen_sonidos)
                if barra_musica_rect.collidepoint(event.pos) or music_thumb_rect.collidepoint(event.pos):
                    click_sound.play()
                    active_slider = "music"
                    set_music_volume(event.pos[0])
                elif barra_sonidos_rect.collidepoint(event.pos) or sound_thumb_rect.collidepoint(event.pos):
                    click_sound.play()
                    active_slider = "sound"
                    set_sound_volume(event.pos[0])

            if event.type == pygame.MOUSEMOTION and active_slider:
                if active_slider == "music":
                    set_music_volume(event.pos[0])
                elif active_slider == "sound":
                    set_sound_volume(event.pos[0])

            if event.type == pygame.MOUSEBUTTONUP and active_slider:
                active_slider = None

            volver_btn.handle_event(event)

        volver_btn.draw(screen)
        pygame.display.flip()
        clock.tick(SCREEN_FPS)

    return routes.MENU


def _draw_slider(screen, rect, value, font):
    pygame.draw.rect(screen, SLIDER_BACKGROUND_COLOR, rect, border_radius=12)
    fill_rect = pygame.Rect(rect.x, rect.y, int(rect.width * value), rect.height)
    pygame.draw.rect(screen, SLIDER_FILL_COLOR, fill_rect, border_radius=12)
    pygame.draw.rect(screen, SLIDER_BORDER_COLOR, rect, 2, border_radius=12)

    thumb_x = rect.x + int(rect.width * value)
    pygame.draw.circle(screen, SLIDER_THUMB_COLOR, (thumb_x, rect.centery), SLIDER_THUMB_RADIUS)
    pygame.draw.circle(screen, SLIDER_BORDER_COLOR, (thumb_x, rect.centery), SLIDER_THUMB_RADIUS, 2)

    percent = font.render(f"{int(value * 100)}%", True, config.INK)
    screen.blit(percent, (rect.right + 18, rect.y - 2))


def _value_from_slider_x(rect, mouse_x):
    relative_x = mouse_x - rect.x
    return max(0, min(1, relative_x / rect.width))


def _thumb_hit_rect(rect, value):
    thumb_x = rect.x + int(rect.width * value)
    return pygame.Rect(
        thumb_x - SLIDER_THUMB_RADIUS,
        rect.centery - SLIDER_THUMB_RADIUS,
        SLIDER_THUMB_RADIUS * 2,
        SLIDER_THUMB_RADIUS * 2,
    )
