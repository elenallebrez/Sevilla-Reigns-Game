import pygame

from screens import routes
from ui.button import Button


MENU_FPS = 60
TITLE_COLOR = (9, 45, 134)
BUTTON_WIDTH_RATIO = 0.15
BUTTON_MIN_WIDTH = 190
BUTTON_MAX_WIDTH = 240
BUTTON_HEIGHT_RATIO = 0.065
BUTTON_MIN_HEIGHT = 48
BUTTON_MAX_HEIGHT = 58
BUTTON_GAP_RATIO = 0.03


def start_screen(screen, WIDTH, HEIGHT, FONT, SUPER_FONT, background_image):
    clock = pygame.time.Clock()
    next_screen = None
    focused_index = 0

    def start_game():
        nonlocal next_screen
        next_screen = routes.GAME

    def show_tutorial():
        nonlocal next_screen
        next_screen = routes.TUTORIAL

    def show_settings():
        nonlocal next_screen
        next_screen = routes.SETTINGS

    def show_credits():
        nonlocal next_screen
        next_screen = routes.CREDITS

    def quit_game():
        nonlocal next_screen
        next_screen = routes.QUIT

    button_width = max(BUTTON_MIN_WIDTH, min(BUTTON_MAX_WIDTH, int(WIDTH * BUTTON_WIDTH_RATIO)))
    button_height = max(BUTTON_MIN_HEIGHT, min(BUTTON_MAX_HEIGHT, int(HEIGHT * BUTTON_HEIGHT_RATIO)))
    gap = int(WIDTH * BUTTON_GAP_RATIO)
    left_x = WIDTH // 2 - button_width - gap // 2
    right_x = WIDTH // 2 + gap // 2
    row_1_y = int(HEIGHT * 0.47)
    row_2_y = row_1_y + button_height + int(HEIGHT * 0.03)
    exit_y = row_2_y + button_height + int(HEIGHT * 0.055)

    buttons = [
        Button("Comenzar", left_x, row_1_y, button_width, button_height, start_game, FONT, variant="primary", icon="tower"),
        Button("Tutorial", right_x, row_1_y, button_width, button_height, show_tutorial, FONT, icon="book"),
        Button("Ajustes", left_x, row_2_y, button_width, button_height, show_settings, FONT, icon="gear"),
        Button("Créditos", right_x, row_2_y, button_width, button_height, show_credits, FONT, icon="flower"),
        Button("Salir", WIDTH // 2 - button_width // 2, exit_y, button_width, button_height, quit_game, FONT, variant="danger", icon="door"),
    ]

    while next_screen is None:
        for index, button in enumerate(buttons):
            button.set_focused(index == focused_index)

        screen.blit(background_image, (0, 0))

        title = SUPER_FONT.render("Tú Verás Lo Que Haces", True, TITLE_COLOR)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, int(HEIGHT * 0.2)))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return routes.QUIT
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_DOWN, pygame.K_RIGHT, pygame.K_TAB):
                    focused_index = (focused_index + 1) % len(buttons)
                elif event.key in (pygame.K_UP, pygame.K_LEFT):
                    focused_index = (focused_index - 1) % len(buttons)
            for button in buttons:
                button.handle_event(event)

        for button in buttons:
            button.draw(screen)

        pygame.display.flip()
        clock.tick(MENU_FPS)

    return next_screen
