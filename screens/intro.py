import pygame
import sys

def mostrar_carta_introductoria(screen, FONT, BIG_FONT, WIDTH, HEIGHT, background_image):
    clock = pygame.time.Clock()
    esperando = True

    texto1 = "¡Has ganado las elecciones!"
    texto2 = "Ahora eres el nuevo alcalde de Sevilla."
    texto3 = "Pulsa <- o -> para comenzar tu mandato."

    # Crear caja tipo pergamino
    caja_ancho = WIDTH - 100
    caja_alto = 250
    caja_x = 50
    caja_y = HEIGHT // 2 - caja_alto // 2

    while esperando:
        screen.blit(background_image, (0, 0))

        # Dibujar caja blanca con bordes redondeados
        caja_surface = pygame.Surface((caja_ancho, caja_alto), pygame.SRCALPHA)
        pygame.draw.rect(caja_surface, (255, 255, 255, 235), (0, 0, caja_ancho, caja_alto), border_radius=20)
        screen.blit(caja_surface, (caja_x, caja_y))

        # Títulos con separación y centrado
        y = caja_y + 30
        for texto in [texto1, texto2]:
            render = BIG_FONT.render(texto, True, (9, 45, 134))
            screen.blit(render, (WIDTH // 2 - render.get_width() // 2, y))
            y += 70

        # Instrucción con color más tenue
        texto_instruccion = FONT.render(texto3, True, (100, 100, 100))
        screen.blit(texto_instruccion, (WIDTH // 2 - texto_instruccion.get_width() // 2, y + 20))

        # Manejo de eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                    esperando = False

        pygame.display.flip()
        clock.tick(60)
