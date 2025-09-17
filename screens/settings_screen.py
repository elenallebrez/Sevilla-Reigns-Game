import pygame
import sys
from ui.button import Button
from core.sounds import cambiar_volumen, cambiar_volumen_sonidos, click_sound
from config import WIDTH, HEIGHT, BIG_FONT

def settings_screen(screen, WIDTH, HEIGHT, FONT, background_image):
    clock = pygame.time.Clock()
    running = True

    volumen_musica = 0.5
    volumen_sonidos = 0.5
    cambiar_volumen(volumen_musica)
    cambiar_volumen_sonidos(volumen_sonidos)

    # Barras
    barra_musica_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 60, 200, 20)
    barra_sonidos_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 20, 200, 20)

    def go_back():
        nonlocal running
        click_sound.play()
        running = False

    volver_btn = Button("Volver", WIDTH // 2 - 100, HEIGHT - 180, 200, 50, go_back, FONT)

    while running:
        screen.blit(background_image, (0, 0))

        # Títulos
        titulo = BIG_FONT.render("Ajustes", True, (9, 45, 134))
        screen.blit(titulo, (WIDTH // 2 - titulo.get_width() // 2, 140))

        texto_musica = FONT.render("Volumen musica", True, (9, 45, 134))
        screen.blit(texto_musica, (WIDTH // 2 - texto_musica.get_width() // 2, HEIGHT // 2 - 100))

        texto_sonidos = FONT.render("Volumen efectos", True, (9, 45, 134))
        screen.blit(texto_sonidos, (WIDTH // 2 - texto_sonidos.get_width() // 2, HEIGHT // 2 - 20))

        # Dibujar barras
        pygame.draw.rect(screen, (100, 100, 100), barra_musica_rect)
        pygame.draw.rect(screen, (0, 150, 0), (barra_musica_rect.x, barra_musica_rect.y, barra_musica_rect.width * volumen_musica, barra_musica_rect.height))

        pygame.draw.rect(screen, (100, 100, 100), barra_sonidos_rect)
        pygame.draw.rect(screen, (0, 150, 0), (barra_sonidos_rect.x, barra_sonidos_rect.y, barra_sonidos_rect.width * volumen_sonidos, barra_sonidos_rect.height))

        # Eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if barra_musica_rect.collidepoint(event.pos):
                    click_sound.play()
                    volumen_musica = (event.pos[0] - barra_musica_rect.x) / barra_musica_rect.width
                    cambiar_volumen(volumen_musica)

                elif barra_sonidos_rect.collidepoint(event.pos):
                    click_sound.play()
                    volumen_sonidos = (event.pos[0] - barra_sonidos_rect.x) / barra_sonidos_rect.width
                    cambiar_volumen_sonidos(volumen_sonidos)

            volver_btn.handle_event(event)

        volver_btn.draw(screen)
        pygame.display.flip()
        clock.tick(60)

    return "menu"
