import pygame
import sys
from ui.button import Button

def tutorial_screen(screen, WIDTH, HEIGHT, FONT, background_image):
    clock = pygame.time.Clock()
    running = True

    def go_back():
        nonlocal running
        running = False

    # Botón "Volver"
    back_button = Button("Volver", WIDTH//2 - 100, HEIGHT - 180, 200, 50, go_back, FONT)

    # Texto explicativo del tutorial
    tutorial_text = [
        "Has sido elegido alcalde de Sevilla.",
        "",
        "Desliza a la izquierda o derecha",
        "para tomar decisiones.",
        "",
        "Cada decision afecta a 4 barras:",
        "Tradicion, Vecindario, Dinero y Turismo.",
        "",
        "Si una barra llega a 0 o 100... ¡SE ACABO!",
        "",
        "Tu Veras Lo Que Haces",
    ]

    # Bucle de pantalla
    while running:
        screen.blit(background_image, (0, 0))

        # Caja translúcida para el tutorial
        #box_width = WIDTH - 100
        #box_height = HEIGHT - 200
        #box_surface = pygame.Surface((box_width, box_height), pygame.SRCALPHA)
        #pygame.draw.rect(box_surface, (255, 255, 255, 220), box_surface.get_rect(), border_radius=20)
        #screen.blit(box_surface, (50, 70))

        # Renderizado del texto
        y_offset = 100
        for line in tutorial_text:
            rendered = FONT.render(line, True, (9, 45, 134))
            screen.blit(rendered, (WIDTH//2 - rendered.get_width()//2, y_offset))
            y_offset += 40

        # Eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            back_button.handle_event(event)

        back_button.draw(screen)
        pygame.display.flip()
        clock.tick(60)

    return "menu"
