from sevilla_reigns.domain.entities.game_state import GameState


CARDS_PER_REELECTION = 30


class GameSession:
    def __init__(self, event_manager, game_state: GameState | None = None) -> None:
        self.event_manager = event_manager
        self.game_state = game_state or GameState()
        self.current_event = None
        self.cards_played = 0
        self.last_effects = {}

    def start(self):
        self.event_manager.reset_progress()
        self.game_state.reset()
        self.cards_played = 0
        self.last_effects = {}
        self.current_event = self.event_manager.select_event()
        return self.current_event

    def advance_event(self):
        self.cards_played += 1
        should_show_reelection = self.cards_played >= CARDS_PER_REELECTION

        if should_show_reelection:
            self.game_state.reset()
            self.cards_played = 0

        self.current_event = self.event_manager.select_event()
        return self.current_event, should_show_reelection
