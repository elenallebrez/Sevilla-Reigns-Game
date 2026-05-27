from dataclasses import dataclass


DEFAULT_VOLUME = 0.5


@dataclass
class SettingsState:
    music_volume: float = DEFAULT_VOLUME
    sound_volume: float = DEFAULT_VOLUME
