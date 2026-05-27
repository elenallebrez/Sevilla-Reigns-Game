import sys
from pathlib import Path

import pygame


SRC_PATH = Path(__file__).resolve().parent / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from sevilla_reigns.main.app import GameApp
from sevilla_reigns.main.runtime import initialize_pygame


def main():
    initialize_pygame(fullscreen="--windowed" not in sys.argv)
    app = GameApp()
    app.run()
    pygame.quit()


if __name__ == "__main__":
    main()
