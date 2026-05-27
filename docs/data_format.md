# Data Format

Game content lives in `data/eventos.json` and `data/motivos_muerte.json`.

## Event Records

Each event in `data/eventos.json` must include:

- `id`: unique string identifier.
- `title`: card title shown to the player.
- `description`: card body text.
- `options`: exactly two options, left first and right second.

Optional event fields:

- `image`: filename under `resources/images/`.
- `requisitos`: list of event IDs that must be unlocked before this event can appear.

Each option must include:

- `text`: option label.
- `effects`: object mapping stat keys to integer deltas.

Optional option fields:

- `desbloquea`: event ID or list of event IDs unlocked when this option is chosen.

## Stats

Valid stat keys are:

- `religion`: player-facing label `Tradicion`.
- `people`: player-facing label `Vecindario`.
- `money`: player-facing label `Dinero`.
- `tourism`: player-facing label `Turismo`.

Stats start at `50`, clamp between `0` and `100`, and the game ends when a stat reaches either boundary.

If multiple stats reach a boundary in the same decision, death priority is deterministic:

1. `religion`
2. `people`
3. `money`
4. `tourism`

## Unlock Scope

Unlock state is session-scoped. Starting a new game calls `EventManager.reset_progress()` through `GameSession.start()`, so activated and unlocked events are reset for the new run.

Follow-up events are only unlocked if the player chooses the option containing `desbloquea`. If that option is never chosen, those follow-up events remain unavailable for that session.

## Death Reasons

`data/motivos_muerte.json` must include every valid stat key. Each stat must define:

- `zero`: non-empty list of death reasons for value `0`.
- `hundred`: non-empty list of death reasons for value `100`.

Each death reason must include:

- `motivo`: text shown on the final screen.
- `imagen`: filename under `resources/images/`.

## Assets

Image filenames should use lowercase snake_case. Every image referenced by JSON must exist under `resources/images/`.

## Validation

Run this before changing content:

```bash
python scripts/validate_data.py
python -m pytest tests/test_data_integrity.py
```
