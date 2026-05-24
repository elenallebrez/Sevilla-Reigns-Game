from core.settings_state import DEFAULT_VOLUME, SettingsState


def test_settings_state_defaults_to_mid_volume():
    settings = SettingsState()

    assert settings.music_volume == DEFAULT_VOLUME
    assert settings.sound_volume == DEFAULT_VOLUME
