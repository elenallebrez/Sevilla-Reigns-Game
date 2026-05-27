from dataclasses import dataclass, field


StatName = str
Stats = dict[StatName, int]

MIN_STAT_VALUE = 0
MAX_STAT_VALUE = 100
DEFAULT_STAT_VALUE = 50

DEFAULT_STATS: Stats = {
    "religion": DEFAULT_STAT_VALUE,
    "people": DEFAULT_STAT_VALUE,
    "money": DEFAULT_STAT_VALUE,
    "tourism": DEFAULT_STAT_VALUE,
}

END_STAT_PRIORITY = ("religion", "people", "money", "tourism")
STAT_LABELS = {
    "religion": "Tradición",
    "people": "Vecindario",
    "money": "Dinero",
    "tourism": "Turismo",
}


def get_default_stats() -> Stats:
    return DEFAULT_STATS.copy()


@dataclass
class GameState:
    stats: Stats = field(default_factory=get_default_stats)

    def reset(self) -> None:
        self.stats = get_default_stats()

    def apply_effects(self, effects: dict[str, int]) -> list[str]:
        unknown_stats = []
        for stat, change in effects.items():
            if stat not in self.stats:
                unknown_stats.append(stat)
                continue

            self.stats[stat] = max(
                MIN_STAT_VALUE,
                min(MAX_STAT_VALUE, self.stats[stat] + change),
            )

        return unknown_stats

    def get_end_stat(self) -> str | None:
        for stat in END_STAT_PRIORITY:
            value = self.stats.get(stat, DEFAULT_STAT_VALUE)
            if value <= MIN_STAT_VALUE or value >= MAX_STAT_VALUE:
                return stat

        return None
