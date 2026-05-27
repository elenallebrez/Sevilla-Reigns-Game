from sevilla_reigns.application.decision_resolver import resolve_decision
from sevilla_reigns.domain.entities.game_state import GameState


class FakeEventManager:
    def apply_decision(self, event, option_index):
        assert event == "event"
        assert option_index == 1
        return {"people": -10}


def test_resolve_decision_applies_effects_once_and_returns_them():
    game_state = GameState()

    effects = resolve_decision(FakeEventManager(), game_state, "event", 1)

    assert effects == {"people": -10}
    assert game_state.stats["people"] == 40
