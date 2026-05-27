import pygame

from sevilla_reigns.config import settings as config

def reproducir_musica():
    ruta_musica = config.RESOURCE_PATH / "sounds" / "Bajo el Sol de Sevilla.mp3"
    pygame.mixer.music.load(ruta_musica)
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)

def cambiar_volumen(volumen: float):
    volumen = max(0.0, min(1.0, volumen))
    pygame.mixer.music.set_volume(volumen)

click_sound = pygame.mixer.Sound(str(config.RESOURCE_PATH / "sounds" / "mouse-click.wav"))
swipe_sound = pygame.mixer.Sound(str(config.RESOURCE_PATH / "sounds" / "swipe.wav"))
page_sound = pygame.mixer.Sound(str(config.RESOURCE_PATH / "sounds" / "page_swipe.wav"))
fail_sound = pygame.mixer.Sound(str(config.RESOURCE_PATH / "sounds" / "fail.wav"))

def cambiar_volumen_sonidos(volumen: float):
    volumen = max(0.0, min(1.0, volumen))
    click_sound.set_volume(volumen)
    swipe_sound.set_volume(volumen)
    page_sound.set_volume(volumen)

def reproducir_muerte():
    muerte_sound = config.RESOURCE_PATH / "sounds" / "gameOver.mp3"
    pygame.mixer.music.load(muerte_sound)
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)
