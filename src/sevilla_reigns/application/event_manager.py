import json
import random
from pathlib import Path

from sevilla_reigns.domain.entities.event import Event


class EventManager:
    def __init__(self, json_path: str | Path) -> None:
        self.original_events = self.load_events(json_path)
        self.activated_event_ids: set[str] = set()
        self.unlocked_event_ids: set[str] = set()
        self.reset_events()

    def reset_events(self) -> None:
        self.available_events = self.original_events[:]
        random.shuffle(self.available_events)

    def reset_progress(self) -> None:
        self.activated_event_ids.clear()
        self.unlocked_event_ids.clear()
        self.reset_events()

    def load_events(self, path: str | Path) -> list[Event]:
        with open(path, "r", encoding="utf-8") as file:
            raw_events = json.load(file)

        return [Event(**event) for event in raw_events]

    def get_available_events(self) -> list[Event]:
        possible_events = []
        for event in self.available_events:
            if event.id in self.activated_event_ids:
                continue

            if event.requirements and not all(
                requirement in self.unlocked_event_ids
                for requirement in event.requirements
            ):
                continue

            possible_events.append(event)

        return possible_events

    def select_event(self) -> Event | None:
        possible_events = self.get_available_events()

        if not possible_events:
            self.activated_event_ids.clear()
            self.reset_events()
            possible_events = self.get_available_events()

        if not possible_events:
            return None

        selected = random.choice(possible_events)
        self.available_events.remove(selected)
        return selected

    def apply_decision(self, event: Event, option_index: int) -> dict[str, int]:
        option = event.options[option_index]
        self.activated_event_ids.add(event.id)
        self.unlocked_event_ids.add(event.id)

        if option.unlocks:
            self._unlock_events(option.unlocks)

        return option.effects

    def _unlock_events(self, unlocks: str | list[str]) -> None:
        if isinstance(unlocks, list):
            self.unlocked_event_ids.update(unlocks)
            return

        self.unlocked_event_ids.add(unlocks)
