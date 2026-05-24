from core.effects import apply_effects, get_end_stat
from core.game_state import GameState, get_default_stats


def test_apply_effects_updates_known_stats():
    game_state = GameState()

    apply_effects(game_state, {"people": 10, "money": -15})

    assert game_state.stats["people"] == 60
    assert game_state.stats["money"] == 35


def test_apply_effects_clamps_stats_between_zero_and_hundred():
    game_state = GameState()

    apply_effects(game_state, {"people": 200, "money": -200})

    assert game_state.stats["people"] == 100
    assert game_state.stats["money"] == 0


def test_apply_effects_ignores_unknown_stats(capsys):
    game_state = GameState()

    unknown_stats = apply_effects(game_state, {"unknown": 50})
    captured = capsys.readouterr()

    assert unknown_stats == ["unknown"]
    assert game_state.stats == get_default_stats()
    assert "Stat desconocida: unknown" in captured.out


def test_get_end_stat_returns_first_stat_at_limit():
    game_state = GameState()
    game_state.stats["religion"] = 0

    assert get_end_stat(game_state) == "religion"


def test_get_end_stat_uses_documented_priority_when_multiple_stats_fail():
    game_state = GameState()
    game_state.stats["money"] = 0
    game_state.stats["people"] = 100

    assert get_end_stat(game_state) == "people"


def test_get_end_stat_returns_none_when_no_stat_is_at_limit():
    assert get_end_stat(GameState()) is None
