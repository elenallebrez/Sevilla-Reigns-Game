import random

import pygame

from sevilla_reigns.config import settings as config
from sevilla_reigns.presentation.screens import routes


DEFAULT_TILE_SIZE = 150
DEFAULT_TRANSITION_FPS = 60
DEFAULT_TILES_PER_STEP = 6
DEFAULT_PAUSE_BEFORE_UNCOVER = 0.15
FALLBACK_TILE_COLOR = (50, 50, 50)
TILE_IMAGE_NAME = "azulejo.jpg"


def slide_transition(
    screen,
    clock,
    next_screen_name,
    tile_size: int = DEFAULT_TILE_SIZE,
    fps: int = DEFAULT_TRANSITION_FPS,
    tiles_per_step: int = DEFAULT_TILES_PER_STEP,
    randomize: bool = True,
    draw_screen_func=None,
    next_screen_surface=None,
    pause_before_uncover: float = DEFAULT_PAUSE_BEFORE_UNCOVER,
):
    width, height = screen.get_size()
    tile_image = _load_tile_image(tile_size)
    tiles = [(x, y) for y in range(0, height, tile_size) for x in range(0, width, tile_size)]
    cover_order = tiles[:]

    if randomize:
        random.shuffle(cover_order)

    snapshot_old = screen.copy()
    if _cover_screen(screen, clock, snapshot_old, tile_image, cover_order, tiles_per_step, fps) == routes.QUIT:
        return routes.QUIT

    next_surface = _build_next_surface(
        width,
        height,
        next_screen_name,
        draw_screen_func,
        next_screen_surface,
    )
    snapshot_next = next_surface.copy()

    screen.blit(snapshot_next, (0, 0))
    for x, y in cover_order:
        screen.blit(tile_image, (x, y))
    pygame.display.flip()

    if _pause_before_uncover(clock, fps, pause_before_uncover) == routes.QUIT:
        return routes.QUIT

    if _uncover_screen(screen, clock, snapshot_next, tile_image, cover_order, tiles_per_step, fps) == routes.QUIT:
        return routes.QUIT

    screen.blit(snapshot_next, (0, 0))
    pygame.display.flip()

    return next_screen_name


def _load_tile_image(tile_size: int):
    try:
        tile_image = pygame.image.load(str(config.IMG_PATH / TILE_IMAGE_NAME)).convert()
        return pygame.transform.scale(tile_image, (tile_size, tile_size))
    except (FileNotFoundError, pygame.error) as exc:
        print(f"No se pudo cargar el azulejo de transicion '{TILE_IMAGE_NAME}': {exc}")
        fallback = pygame.Surface((tile_size, tile_size))
        fallback.fill(FALLBACK_TILE_COLOR)
        return fallback


def _cover_screen(screen, clock, snapshot_old, tile_image, cover_order, tiles_per_step: int, fps: int):
    covered = 0
    total = len(cover_order)

    while covered < total:
        if _consume_quit_event() == routes.QUIT:
            return routes.QUIT

        covered = min(total, covered + tiles_per_step)
        screen.blit(snapshot_old, (0, 0))
        for x, y in cover_order[:covered]:
            screen.blit(tile_image, (x, y))
        pygame.display.flip()
        clock.tick(fps)

    return None


def _build_next_surface(width, height, next_screen_name, draw_screen_func, next_screen_surface):
    if next_screen_surface is not None:
        return next_screen_surface

    if draw_screen_func is None:
        raise ValueError(
            "slide_transition necesita draw_screen_func(surface, name) "
            "o next_screen_surface."
        )

    next_surface = pygame.Surface((width, height)).convert()
    draw_screen_func(next_surface, next_screen_name)
    return next_surface


def _pause_before_uncover(clock, fps: int, pause_before_uncover: float):
    if pause_before_uncover <= 0:
        return None

    start_ticks = pygame.time.get_ticks()
    wait_ms = int(pause_before_uncover * 1000)
    while pygame.time.get_ticks() - start_ticks < wait_ms:
        if _consume_quit_event() == routes.QUIT:
            return routes.QUIT
        clock.tick(fps)

    return None


def _uncover_screen(screen, clock, snapshot_next, tile_image, cover_order, tiles_per_step: int, fps: int):
    remaining_tiles = cover_order[:]

    while remaining_tiles:
        if _consume_quit_event() == routes.QUIT:
            return routes.QUIT

        del remaining_tiles[: min(tiles_per_step, len(remaining_tiles))]

        screen.blit(snapshot_next, (0, 0))
        for x, y in remaining_tiles:
            screen.blit(tile_image, (x, y))
        pygame.display.flip()
        clock.tick(fps)

    return None


def _consume_quit_event():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return routes.QUIT

    return None
