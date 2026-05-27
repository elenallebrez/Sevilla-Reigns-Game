import pygame

import config


def load_font(path, size: int, bold: bool = False) -> pygame.font.Font:
    font = pygame.font.Font(str(path), size)
    font.set_bold(bold)
    return font


def initialize_pygame(fullscreen=True):
    if config.screen is not None:
        return config.screen

    pygame.init()

    flags = pygame.FULLSCREEN if fullscreen else 0
    config.screen = pygame.display.set_mode((0, 0), flags)
    config.WIDTH, config.HEIGHT = config.screen.get_size()
    pygame.display.set_caption("Tú Verás Lo Que Haces")

    config.FONT_TITLE = load_font(config.CINZEL_BOLD_PATH, 68, bold=True)
    config.FONT_EVENT_TITLE = load_font(config.CINZEL_SEMIBOLD_PATH, 40, bold=True)
    config.FONT_BUTTON = load_font(config.CINZEL_SEMIBOLD_PATH, 22, bold=True)
    config.FONT_BODY = load_font(config.CORMORANT_REGULAR_PATH, 28)
    config.FONT_BODY_MEDIUM = load_font(config.CORMORANT_MEDIUM_PATH, 30)
    config.FONT_SMALL = load_font(config.CORMORANT_REGULAR_PATH, 23)
    config.FONT_CATEGORY = load_font(config.CINZEL_SEMIBOLD_PATH, 20, bold=True)

    config.SUPER_FONT = config.FONT_TITLE
    config.BIG_FONT = config.FONT_EVENT_TITLE
    config.MEDIUM_FONT = config.FONT_BODY_MEDIUM
    config.FONT = config.FONT_BODY

    config.icons_empty = {
        "religion": pygame.image.load(str(config.IMG_PATH / "religion3.png")),
        "people": pygame.image.load(str(config.IMG_PATH / "people3.png")),
        "money": pygame.image.load(str(config.IMG_PATH / "money3.png")),
        "tourism": pygame.image.load(str(config.IMG_PATH / "tourism3.png")),
    }

    config.icons_mask = {
        "religion": pygame.image.load(str(config.IMG_PATH / "religion_sil.png")),
        "people": pygame.image.load(str(config.IMG_PATH / "people_sil.png")),
        "money": pygame.image.load(str(config.IMG_PATH / "money_sil.png")),
        "tourism": pygame.image.load(str(config.IMG_PATH / "tourism_sil.png")),
    }

    config.clock = pygame.time.Clock()
    return config.screen
