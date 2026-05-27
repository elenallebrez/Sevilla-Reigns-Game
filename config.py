from pathlib import Path

BASE_PATH = Path(__file__).resolve().parent
DATA_PATH = BASE_PATH / "data"
RESOURCE_PATH = BASE_PATH / "resources"
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
BLUE_AZULEJO = (9, 45, 134)
ALBERO = (246, 205, 116)
ALBERO_LIGHT = (255, 235, 174)
CAL_WHITE = (255, 252, 244)
CARD_IVORY = (255, 249, 232)
CLAVEL_RED = (166, 36, 42)
OLIVE_GREEN = (74, 112, 66)
INK = (38, 29, 23)
TILE_SHADOW = (45, 35, 24)

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
