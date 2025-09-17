import pygame
import os
import json

# Inicializar pygame (para fuentes e imágenes)
pygame.init()

# === Dimensiones pantalla ===
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WIDTH, HEIGHT = screen.get_size()
pygame.display.set_caption("Tú Verás Lo Que Haces")
FPS = 60

# === Colores ===
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BG_COLOR = (230, 220, 200)
BAR_COLOR = (100, 200, 100)
BLUE_AZULEJO = (9, 45, 134)

# === Fuentes ===
FONT_PATH = "resources/fonts/andalus.ttf"
SUPER_FONT = pygame.font.Font(FONT_PATH, 80)
BIG_FONT = pygame.font.Font(FONT_PATH, 48)
MEDIUM_FONT = pygame.font.Font(FONT_PATH, 36)
FONT = pygame.font.Font(FONT_PATH, 28)

# === Recursos (paths e imágenes) ===
BASE_PATH = os.path.dirname(__file__)
IMG_PATH = os.path.join(BASE_PATH, "resources", "images")

icons_empty = {
    "religion": pygame.image.load(os.path.join(os.path.dirname(__file__),"resources", "images", "religion3.png")),
    "people": pygame.image.load(os.path.join(os.path.dirname(__file__),"resources", "images", "people3.png")),
    "money": pygame.image.load(os.path.join(os.path.dirname(__file__),"resources", "images", "money3.png")),
    "army": pygame.image.load(os.path.join(os.path.dirname(__file__),"resources", "images", "army3.png")),
}

icons_mask = {
    "religion": pygame.image.load(os.path.join(os.path.dirname(__file__),"resources", "images", "religionSil.png")),
    "people": pygame.image.load(os.path.join(os.path.dirname(__file__),"resources", "images", "peopleSil.png")),
    "money": pygame.image.load(os.path.join(os.path.dirname(__file__),"resources", "images", "moneySil.png")),
    "army": pygame.image.load(os.path.join(os.path.dirname(__file__),"resources", "images", "armySil.png")),
}

# === Eventos ===
DATA_PATH = os.path.join(BASE_PATH, "data")
with open(os.path.join(DATA_PATH, "eventos.json"), "r", encoding="utf-8") as f:
    eventos = json.load(f)

# === Clock (FPS) ===
clock = pygame.time.Clock()
