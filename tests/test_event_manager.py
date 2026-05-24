import json

from core.event_manager import EventManager


def write_events(tmp_path, events):
    events_path = tmp_path / "eventos.json"
    events_path.write_text(json.dumps(events), encoding="utf-8")
    return events_path


def make_event(event_id, requisitos=None, desbloquea=None):
    option = {
        "text": "Aceptar",
        "effects": {"people": 1},
    }
    if desbloquea is not None:
        option["desbloquea"] = desbloquea

    return {
        "id": event_id,
        "title": event_id,
        "description": event_id,
        "requisitos": requisitos or [],
        "options": [
            option,
            {
                "text": "Rechazar",
                "effects": {"people": -1},
            },
        ],
    }


def test_selection_restarts_without_recursion_when_events_are_exhausted(tmp_path):
    manager = EventManager(write_events(tmp_path, [make_event("only_event")]))

    selected_ids = []
    for _ in range(5):
        event = manager.select_event()
        selected_ids.append(event.id)
        manager.apply_decision(event, 0)

    assert selected_ids == ["only_event"] * 5


def test_requirements_block_events_until_unlocked(tmp_path):
    manager = EventManager(
        write_events(
            tmp_path,
            [
                make_event("base", desbloquea="follow_up"),
                make_event("follow_up", requisitos=["base"]),
            ],
        )
    )

    first_event = manager.select_event()
    assert first_event.id == "base"

    manager.apply_decision(first_event, 0)
    second_event = manager.select_event()

    assert second_event.id == "follow_up"


def test_list_unlocks_are_supported(tmp_path):
    manager = EventManager(
        write_events(
            tmp_path,
            [
                make_event("base", desbloquea=["a", "b"]),
                make_event("a", requisitos=["base"]),
                make_event("b", requisitos=["base"]),
            ],
        )
    )

    event = manager.select_event()
    manager.apply_decision(event, 0)

    assert {"a", "b"}.issubset(manager.unlocked_event_ids)


def test_apply_decision_returns_selected_option_effects(tmp_path):
    manager = EventManager(write_events(tmp_path, [make_event("base")]))
    event = manager.select_event()

    effects = manager.apply_decision(event, 1)

    assert effects == {"people": -1}
