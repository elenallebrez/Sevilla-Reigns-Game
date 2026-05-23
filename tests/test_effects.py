import pytest

from core.effects import aplicar_efectos, check_fin
from core.game_state import get_default_stats, stats


@pytest.fixture(autouse=True)
def reset_stats():
    stats.clear()
    stats.update(get_default_stats())


def test_aplicar_efectos_updates_known_stats():
    aplicar_efectos({"people": 10, "money": -15})

    assert stats["people"] == 60
    assert stats["money"] == 35


def test_aplicar_efectos_clamps_stats_between_zero_and_hundred():
    aplicar_efectos({"people": 200, "money": -200})

    assert stats["people"] == 100
    assert stats["money"] == 0


def test_aplicar_efectos_ignores_unknown_stats(capsys):
    aplicar_efectos({"unknown": 50})

    captured = capsys.readouterr()

    assert stats == get_default_stats()
    assert "Stat desconocida: unknown" in captured.out


def test_check_fin_returns_first_stat_at_limit():
    stats["religion"] = 0

    assert check_fin() == "religion"


def test_check_fin_returns_none_when_no_stat_is_at_limit():
    assert check_fin() is None
