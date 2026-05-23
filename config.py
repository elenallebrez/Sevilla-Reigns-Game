from pathlib import Path

import pygame

BASE_PATH = Path(__file__).resolve().parent
DATA_PATH = BASE_PATH / "data"
RESOURCE_PATH = BASE_PATH / "resources"
IMG_PATH = RESOURCE_PATH / "images"
FONT_PATH = RESOURCE_PATH / "fonts" / "andalus.ttf"

FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BG_COLOR = (230, 220, 200)
BAR_COLOR = (100, 200, 100)
BLUE_AZULEJO = (9, 45, 134)

WIDTH = 0
HEIGHT = 0
screen = None
clock = None

SUPER_FONT = None
BIG_FONT = None
MEDIUM_FONT = None
FONT = None

icons_empty = {}
icons_mask = {}


def initialize_pygame(fullscreen=True):
    global WIDTH, HEIGHT, screen, clock
    global SUPER_FONT, BIG_FONT, MEDIUM_FONT, FONT
    global icons_empty, icons_mask

    if screen is not None:
        return screen

    pygame.init()

    flags = pygame.FULLSCREEN if fullscreen else 0
    screen = pygame.display.set_mode((0, 0), flags)
    WIDTH, HEIGHT = screen.get_size()
    pygame.display.set_caption("Tú Verás Lo Que Haces")

    SUPER_FONT = pygame.font.Font(str(FONT_PATH), 80)
    BIG_FONT = pygame.font.Font(str(FONT_PATH), 48)
    MEDIUM_FONT = pygame.font.Font(str(FONT_PATH), 36)
    FONT = pygame.font.Font(str(FONT_PATH), 28)

    icons_empty = {
        "religion": pygame.image.load(str(IMG_PATH / "religion3.png")),
        "people": pygame.image.load(str(IMG_PATH / "people3.png")),
        "money": pygame.image.load(str(IMG_PATH / "money3.png")),
        "army": pygame.image.load(str(IMG_PATH / "army3.png")),
    }

    icons_mask = {
        "religion": pygame.image.load(str(IMG_PATH / "religionSil.png")),
        "people": pygame.image.load(str(IMG_PATH / "peopleSil.png")),
        "money": pygame.image.load(str(IMG_PATH / "moneySil.png")),
        "army": pygame.image.load(str(IMG_PATH / "armySil.png")),
    }

    clock = pygame.time.Clock()
    return screen
