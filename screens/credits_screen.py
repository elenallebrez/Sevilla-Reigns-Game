import pygame
import sys
from ui.button import Button

def credits_screen(screen, WIDTH, HEIGHT, FONT, background_image):
    clock = pygame.time.Clock()
    running = True

    def go_back():
        nonlocal running
        running = False

    # Botón "Volver"
    back_button = Button("Volver", WIDTH//2 - 100, HEIGHT - 180, 200, 50, go_back, FONT)

    # Texto explicativo del tutorial
    credits_text = [
        "Desarrollado por: Elena Fernandez-Llebrez",
        "",
        "Imagenes y sonidos generados con IA",
        "Gracias por jugar",
        "",
        "Si te ha gustado, te invito a una tapa",
        "Tu Veras Lo Que Haces",
    ]

    line_height = 40
    total_height = len(credits_text) * line_height
    start_y = (HEIGHT - total_height) // 2  # Centrado vertical

    # Bucle de pantalla
    while running:
        screen.blit(background_image, (0, 0))

        # Renderizado del texto
        y_offset = start_y
        for line in credits_text:
            rendered = FONT.render(line, True, (9, 45, 134))
            screen.blit(rendered, (WIDTH//2 - rendered.get_width()//2, y_offset))
            y_offset += line_height

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