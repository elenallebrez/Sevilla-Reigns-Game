from core.effects import apply_effects
from core.game_state import GameState


LEFT_OPTION = 0
RIGHT_OPTION = 1
LEFT_DIRECTION = -1
RIGHT_DIRECTION = 1


def resolve_decision(event_manager, game_state: GameState, event, option_index: int) -> dict[str, int]:
    effects = event_manager.apply_decision(event, option_index)
    apply_effects(game_state, effects)
    return effects
