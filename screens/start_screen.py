import pygame
import os
import sys
from ui.button import Button

def start_screen(screen, WIDTH, HEIGHT, FONT, SUPER_FONT, background_image):
    clock = pygame.time.Clock()
    next_screen = None  # Esto se actualizará cuando pulses un botón

    def start_game():
        nonlocal next_screen
        next_screen = "game"

    def show_tutorial():
        nonlocal next_screen
        next_screen = "tutorial"

    def show_settings():
        nonlocal next_screen
        next_screen = "settings"

    def show_credits():
        nonlocal next_screen
        next_screen = "credits"

    def quit_game():
        pygame.quit()
        sys.exit()

    buttons = [
        # Fila 1
        Button("Comenzar", WIDTH//2 - 220, 360, 200, 50, start_game, FONT),
        Button("Tutorial", WIDTH//2 +  20, 360, 200, 50, show_tutorial, FONT),

        # Fila 2
        Button("Ajustes",  WIDTH//2 - 220, 430, 200, 50, show_settings, FONT),
        Button("Creditos", WIDTH//2 +  20, 430, 200, 50, show_credits, FONT),

        # Botón salir abajo
        Button("Salir",    WIDTH//2 - 100, 520, 200, 50, quit_game, FONT),
    ]


    while next_screen is None:
        screen.blit(background_image, (0, 0))

        title = SUPER_FONT.render("TU VERAS LO QUE HACES", True, (9, 45, 134))
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 150))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            for btn in buttons:
                btn.handle_event(event)

        for btn in buttons:
            btn.draw(screen)

        pygame.display.flip()
        clock.tick(60)

    return next_screen
