import pygame
import sys

from app import GameApp
from runtime import initialize_pygame


def main():
    initialize_pygame(fullscreen="--windowed" not in sys.argv)
    app = GameApp()
    app.run()
    pygame.quit()


if __name__ == "__main__":
    main()
