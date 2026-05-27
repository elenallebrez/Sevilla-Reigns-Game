from sevilla_reigns.application.game_session import CARDS_PER_REELECTION, GameSession
from sevilla_reigns.domain.entities.game_state import GameState


class FakeEventManager:
    def __init__(self):
        self.reset_progress_calls = 0
        self.events = ["event"]

    def reset_progress(self):
        self.reset_progress_calls += 1

    def select_event(self):
        return self.events[0]


def test_start_resets_stats_and_event_manager_progress():
    manager = FakeEventManager()
    game_state = GameState()
    session = GameSession(manager, game_state)
    game_state.stats["people"] = 1

    event = session.start()

    assert event == "event"
    assert manager.reset_progress_calls == 1
    assert game_state.stats["people"] == 50
    assert session.last_effects == {}
    assert session.cards_played == 0


def test_advance_event_marks_reelection_and_resets_counter():
    manager = FakeEventManager()
    session = GameSession(manager)
    session.cards_played = CARDS_PER_REELECTION - 1

    event, should_show_reelection = session.advance_event()

    assert event == "event"
    assert should_show_reelection is True
    assert session.cards_played == 0
