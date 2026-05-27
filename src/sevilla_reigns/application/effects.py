import json
import random
from pathlib import Path

from sevilla_reigns.config import settings as config
from sevilla_reigns.domain.entities.game_state import GameState


DEATH_REASONS_PATH = config.DATA_PATH / "motivos_muerte.json"

with open(DEATH_REASONS_PATH, encoding="utf-8") as file:
    DEATH_REASONS = json.load(file)


def apply_effects(game_state: GameState, effects: dict[str, int]) -> list[str]:
    unknown_stats = game_state.apply_effects(effects)
    for stat in unknown_stats:
        print(f"Stat desconocida: {stat}")

    return unknown_stats


def get_end_stat(game_state: GameState) -> str | None:
    return game_state.get_end_stat()


def get_death_info(stat: str, value: int) -> tuple[str, str | None]:
    if stat not in DEATH_REASONS:
        return "Has abdicado... pero no sabemos por que", None

    limit_key = "zero" if value <= 0 else "hundred"
    options = DEATH_REASONS[stat].get(limit_key, [])

    if not options:
        return "Has muerto de forma misteriosa...", None

    selected = random.choice(options)
    image_path = Path("assets") / "images" / selected["imagen"]
    return selected["motivo"], str(image_path)
