import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EVENTS_PATH = ROOT / "data" / "eventos.json"
DEATH_REASONS_PATH = ROOT / "data" / "motivos_muerte.json"
IMAGES_PATH = ROOT / "assets" / "images"
VALID_STATS = {"religion", "people", "money", "tourism"}


def load_events():
    return json.loads(EVENTS_PATH.read_text(encoding="utf-8"))


def load_death_reasons():
    return json.loads(DEATH_REASONS_PATH.read_text(encoding="utf-8"))


def test_events_have_unique_ids():
    ids = [event["id"] for event in load_events()]

    duplicates = [event_id for event_id, count in Counter(ids).items() if count > 1]

    assert duplicates == []


def test_events_have_exactly_two_options():
    invalid_events = [
        event["id"]
        for event in load_events()
        if len(event.get("options", [])) != 2
    ]

    assert invalid_events == []


def test_event_references_are_valid():
    events = load_events()
    event_ids = {event["id"] for event in events}

    invalid_requirements = []
    invalid_unlocks = []
    for event in events:
        for requirement in event.get("requisitos", []):
            if requirement not in event_ids:
                invalid_requirements.append((event["id"], requirement))

        for option in event.get("options", []):
            unlocks = option.get("desbloquea", [])
            if isinstance(unlocks, str):
                unlocks = [unlocks]

            for unlock in unlocks:
                if unlock not in event_ids:
                    invalid_unlocks.append((event["id"], unlock))

    assert invalid_requirements == []
    assert invalid_unlocks == []


def test_event_stats_are_valid():
    invalid_stats = []
    for event in load_events():
        for option in event.get("options", []):
            for stat in option.get("effects", {}):
                if stat not in VALID_STATS:
                    invalid_stats.append((event["id"], stat))

    assert invalid_stats == []


def test_event_images_exist():
    missing_images = [
        (event["id"], event["image"])
        for event in load_events()
        if event.get("image") and not (IMAGES_PATH / event["image"]).exists()
    ]

    assert missing_images == []


def test_death_reasons_cover_all_stats_and_images_exist():
    death_reasons = load_death_reasons()

    assert set(death_reasons) == VALID_STATS

    missing_images = []
    empty_reason_groups = []
    for stat in VALID_STATS:
        for limit in ("zero", "hundred"):
            reasons = death_reasons[stat].get(limit, [])
            if not reasons:
                empty_reason_groups.append((stat, limit))

            for reason in reasons:
                if not reason.get("motivo"):
                    empty_reason_groups.append((stat, limit))
                if not (IMAGES_PATH / reason["imagen"]).exists():
                    missing_images.append((stat, limit, reason["imagen"]))

    assert empty_reason_groups == []
    assert missing_images == []
