import pygame
import random
import sys

def slide_transition(screen, clock, next_screen_name,
                     tile_size=150, fps=60, tiles_per_step=6,
                     randomize=True, draw_screen_func=None,
                     next_screen_surface=None, pause_before_uncover=0.15):
    """
    Transición tipo "azulejos":
      1) snapshot_old = pantalla actual (la que ya está dibujada)
      2) COVER: se ponen azulejos progresivamente sobre snapshot_old
      3) Se obtiene `next_surface` (llamando draw_screen_func(surface, name) o usando next_screen_surface)
      4) Se cubre COMPLETAMENTE next_surface con azulejos (estado inicial para UNCOVER)
      5) UNCOVER: se van quitando azulejos poco a poco mostrando next_surface debajo
    - draw_screen_func(surface, next_screen_name) debe dibujar la siguiente pantalla SOBRE `surface`.
    - Si no pasas ni draw_screen_func ni next_screen_surface, la función lanzará un error informativo.
    """
    WIDTH, HEIGHT = screen.get_size()

    # ---- cargar tile (fallback si falla la imagen) ----
    try:
        tile_img = pygame.image.load("resources/images/azulejo.jpg").convert()
        tile_img = pygame.transform.scale(tile_img, (tile_size, tile_size))
    except Exception:
        tile_img = pygame.Surface((tile_size, tile_size))
        tile_img.fill((50, 50, 50))

    # ---- grid de tiles ----
    tiles = [(x, y) for y in range(0, HEIGHT, tile_size)
                   for x in range(0, WIDTH, tile_size)]
    cover_order = tiles[:]
    if randomize:
        random.shuffle(cover_order)
    total = len(cover_order)

    # ---- snapshot de la pantalla actual (debe estar ya dibujada por la pantalla actual) ----
    snapshot_old = screen.copy()

    # ---- COVER: poner azulejos progresivamente sobre snapshot_old ----
    covered = 0
    while covered < total:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        covered = min(total, covered + tiles_per_step)

        # redibujamos snapshot_old y los azulejos actuales
        screen.blit(snapshot_old, (0, 0))
        for x, y in cover_order[:covered]:
            screen.blit(tile_img, (x, y))
        pygame.display.flip()
        clock.tick(fps)

    # ---- Obtener la Surface de la siguiente pantalla ----
    if next_screen_surface is None:
        if draw_screen_func is None:
            raise ValueError(
                "slide_transition necesita `draw_screen_func(surface, name)` o `next_screen_surface`.\n"
                "Pasa draw_screen_func que dibuje la pantalla siguiente en la Surface que recibe."
            )
        # crear una surface nueva y pedirle a draw_screen_func que la dibuje
        next_surface = pygame.Surface((WIDTH, HEIGHT)).convert()
        # permitir que draw_screen_func dibuje sobre next_surface
        draw_screen_func(next_surface, next_screen_name)
    else:
        next_surface = next_screen_surface

    # snapshot de la pantalla siguiente (sin azulejos)
    snapshot_next = next_surface.copy()

    # ---- Cubrir por completo la pantalla nueva (para partir desde FULL COVER) ----
    screen.blit(snapshot_next, (0, 0))
    for x, y in cover_order:
        screen.blit(tile_img, (x, y))
    pygame.display.flip()

    # pequeña pausa (sin bloquear eventos)
    if pause_before_uncover > 0:
        t0 = pygame.time.get_ticks()
        wait_ms = int(pause_before_uncover * 1000)
        while pygame.time.get_ticks() - t0 < wait_ms:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            clock.tick(fps)

    # ---- UNCOVER: quitar azulejos poco a poco mostrando snapshot_next ----
    remaining = cover_order[:]  # lista de tiles que todavía están dibujados
    # quitaremos `tiles_per_step` por frame desde el frente (orden cover_order)
    while remaining:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        remove_n = min(tiles_per_step, len(remaining))
        # eliminar los primeros remove_n elementos
        del remaining[:remove_n]

        # dibujar fondo = pantalla nueva, y encima solo los tiles que quedan
        screen.blit(snapshot_next, (0, 0))
        for x, y in remaining:
            screen.blit(tile_img, (x, y))
        pygame.display.flip()
        clock.tick(fps)

    # frame final limpio (pantalla nueva visible)
    screen.blit(snapshot_next, (0, 0))
    pygame.display.flip()

    return next_screen_name
