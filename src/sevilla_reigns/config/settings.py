from pathlib import Path

ROOT_PATH = Path(__file__).resolve().parents[3]
BASE_PATH = ROOT_PATH
DATA_PATH = ROOT_PATH / "data"
RESOURCE_PATH = ROOT_PATH / "assets"
IMG_PATH = RESOURCE_PATH / "images"
ICON_PATH = RESOURCE_PATH / "icons"
FONT_PATH = RESOURCE_PATH / "fonts" / "andalus.ttf"
CINZEL_REGULAR_PATH = RESOURCE_PATH / "fonts" / "Cinzel-Regular.ttf"
CINZEL_SEMIBOLD_PATH = RESOURCE_PATH / "fonts" / "Cinzel-SemiBold.ttf"
CINZEL_BOLD_PATH = RESOURCE_PATH / "fonts" / "Cinzel-Bold.ttf"
CORMORANT_REGULAR_PATH = RESOURCE_PATH / "fonts" / "CormorantGaramond-Regular.ttf"
CORMORANT_MEDIUM_PATH = RESOURCE_PATH / "fonts" / "CormorantGaramond-Medium.ttf"
CORMORANT_SEMIBOLD_PATH = RESOURCE_PATH / "fonts" / "CormorantGaramond-SemiBold.ttf"

FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BG_COLOR = (230, 220, 200)
BAR_COLOR = (100, 200, 100)
from sevilla_reigns.config.theme import (
    ALBERO,
    ALBERO_LIGHT,
    BLUE_AZULEJO,
    CAL_WHITE,
    CARD_IVORY,
    CLAVEL_RED,
    INK,
    OLIVE_GREEN,
    TILE_SHADOW,
)

WIDTH = 0
HEIGHT = 0
screen = None
clock = None

SUPER_FONT = None
BIG_FONT = None
MEDIUM_FONT = None
FONT = None
FONT_TITLE = None
FONT_EVENT_TITLE = None
FONT_BUTTON = None
FONT_BODY = None
FONT_BODY_MEDIUM = None
FONT_SMALL = None
FONT_CATEGORY = None

icons_empty = {}
icons_mask = {}
