import pygame

import config


DISPLAY_FONT_PATH = config.RESOURCE_PATH / "fonts" / "Sevillana-Regular.ttf"
BODY_FONT_CANDIDATES = ("georgia", "segoeui", "arial")


def initialize_pygame(fullscreen=True):
    if config.screen is not None:
        return config.screen

    pygame.init()

    flags = pygame.FULLSCREEN if fullscreen else 0
    config.screen = pygame.display.set_mode((0, 0), flags)
    config.WIDTH, config.HEIGHT = config.screen.get_size()
    pygame.display.set_caption("Tú Verás Lo Que Haces")

    body_font_path = _get_body_font_path()
    display_font_path = str(DISPLAY_FONT_PATH if DISPLAY_FONT_PATH.exists() else body_font_path)

    config.SUPER_FONT = pygame.font.Font(display_font_path, 84)
    config.BIG_FONT = pygame.font.Font(body_font_path, 46)
    config.MEDIUM_FONT = pygame.font.Font(body_font_path, 34)
    config.FONT = pygame.font.Font(body_font_path, 26)

    config.icons_empty = {
        "religion": pygame.image.load(str(config.IMG_PATH / "religion3.png")),
        "people": pygame.image.load(str(config.IMG_PATH / "people3.png")),
        "money": pygame.image.load(str(config.IMG_PATH / "money3.png")),
        "army": pygame.image.load(str(config.IMG_PATH / "army3.png")),
    }

    config.icons_mask = {
        "religion": pygame.image.load(str(config.IMG_PATH / "religion_sil.png")),
        "people": pygame.image.load(str(config.IMG_PATH / "people_sil.png")),
        "money": pygame.image.load(str(config.IMG_PATH / "money_sil.png")),
        "army": pygame.image.load(str(config.IMG_PATH / "army_sil.png")),
    }

    config.clock = pygame.time.Clock()
    return config.screen


def _get_body_font_path() -> str:
    for font_name in BODY_FONT_CANDIDATES:
        font_path = pygame.font.match_font(font_name)
        if font_path:
            return font_path

    return str(config.FONT_PATH)
