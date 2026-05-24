import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EVENTS_PATH = ROOT / "data" / "eventos.json"
DEATH_REASONS_PATH = ROOT / "data" / "motivos_muerte.json"
IMAGES_PATH = ROOT / "resources" / "images"
VALID_STATS = {"religion", "people", "money", "army"}


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def validate_events(events):
    errors = []
    event_ids = [event.get("id") for event in events]
    duplicates = [event_id for event_id, count in Counter(event_ids).items() if count > 1]

    for event_id in duplicates:
        errors.append(f"Duplicate event id: {event_id}")

    known_ids = set(event_ids)
    for event in events:
        event_id = event.get("id", "<missing id>")
        options = event.get("options", [])

        for field in ("id", "title", "description", "options"):
            if field not in event:
                errors.append(f"{event_id}: missing field '{field}'")

        if len(options) != 2:
            errors.append(f"{event_id}: expected exactly 2 options, found {len(options)}")

        if event.get("image") and not (IMAGES_PATH / event["image"]).exists():
            errors.append(f"{event_id}: missing image '{event['image']}'")

        for requirement in event.get("requisitos", []):
            if requirement not in known_ids:
                errors.append(f"{event_id}: unknown requirement '{requirement}'")

        for option in options:
            for stat in option.get("effects", {}):
                if stat not in VALID_STATS:
                    errors.append(f"{event_id}: unknown stat '{stat}'")

            unlocks = option.get("desbloquea", [])
            if isinstance(unlocks, str):
                unlocks = [unlocks]

            for unlock in unlocks:
                if unlock not in known_ids:
                    errors.append(f"{event_id}: unknown unlock '{unlock}'")

    return errors


def validate_death_reasons(death_reasons):
    errors = []
    if set(death_reasons) != VALID_STATS:
        errors.append(
            "Death reason stats do not match valid stats: "
            f"expected {sorted(VALID_STATS)}, found {sorted(death_reasons)}"
        )

    for stat in VALID_STATS:
        for limit in ("zero", "hundred"):
            reasons = death_reasons.get(stat, {}).get(limit, [])
            if not reasons:
                errors.append(f"{stat}.{limit}: no death reasons")

            for reason in reasons:
                if not reason.get("motivo"):
                    errors.append(f"{stat}.{limit}: missing motivo")
                image = reason.get("imagen")
                if not image or not (IMAGES_PATH / image).exists():
                    errors.append(f"{stat}.{limit}: missing image '{image}'")

    return errors


def main():
    errors = []
    errors.extend(validate_events(load_json(EVENTS_PATH)))
    errors.extend(validate_death_reasons(load_json(DEATH_REASONS_PATH)))

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        raise SystemExit(1)

    print("Data validation passed.")


if __name__ == "__main__":
    main()
