# Repository Audit: Sevilla-Reigns-Game

## 1. Executive Summary

| Area | Assessment |
| --- | --- |
| Overall quality | Improved prototype with clearer runtime boundaries, basic tests, and a more maintainable Python/Pygame structure. |
| Main strengths | JSON-driven content, clear high-level folders, safe imports, focused rendering modules, centralized routes, core tests, data validation script, dependency file exists. |
| Main weaknesses | Missing CI/tooling config, weak documentation for architecture/data format, limited UI polish, and some remaining Pygame-heavy UI loops that are best covered by manual QA. |
| Biggest risks | Runtime crashes from missing/corrupt non-image assets, UI layout issues on different displays, untested Pygame frame-loop behavior. |
| Most urgent improvements | Add CI/Ruff config, add broader asset fallbacks for audio/fonts, improve README with screenshots and architecture notes, and add optional Pygame smoke tests. |
| Portfolio readiness | Better than the original audit state, but still needs CI, screenshots/GIF, explicit architecture docs, and a bit more UI polish before it looks strong for recruiters. |

The project is understandable and playable in concept: it is a Reigns-style decision game set in Sevilla, backed by `data/eventos.json` and visual/audio assets under `resources/`. The repository is now closer to a maintainable small Pygame project: startup, routing, session state, rendering, tests, and data validation are separated enough to support the next round of growth.

## 2. Repository Structure and Naming

### Current Structure

```text
Sevilla-Reigns-Game/
  .gitignore
  README.md
  requirements.txt
  config.py
  runtime.py
  app.py
  main.py
  core/
    __init__.py
    decision_resolver.py
    effects.py
    event.py
    event_manager.py
    game_session.py
    game_state.py
    renderer.py
    sounds.py
    transition.py
  rendering/
    __init__.py
    card_renderer.py
    modal_renderer.py
    stats_renderer.py
  data/
    eventos.json
    motivos_muerte.json
  resources/
    fonts/
    images/
    sounds/
  screens/
    __init__.py
    credits_screen.py
    intro_screen.py
    modal_screens.py
    routes.py
    settings_screen.py
    start_screen.py
    tutorial_screen.py
  scripts/
    validate_data.py
  tests/
    test_data_integrity.py
    test_effects.py
    test_event_manager.py
    test_game_session.py
  ui/
    __init__.py
    button.py
```

### What Is Good

- `core/`, `screens/`, `ui/`, `data/`, and `resources/` communicate the broad purpose of each area.
- JSON content is separated from code in `data/`.
- Assets are separated by type under `resources/images`, `resources/sounds`, and `resources/fonts`.
- `requirements.txt` and `.gitignore` exist.
- `__pycache__` files are no longer part of the intended source structure.

### Problems

| Problem | Evidence | Consequence | Recommendation | Resuelto |
| --- | --- | --- | --- | --- |
| Python package boundaries are missing | No `__init__.py` in `core/`, `screens/`, or `ui/` | Imports depend on running from repo root; tests and packaging are harder | Add `__init__.py` files or move code into `src/sevilla_reigns/` | Sí |
| Module name is not idiomatic | `core/event_manager.py` | Python convention is snake_case; name is harder to scan | Rename to `core/event_manager.py` | Sí |
| Screen naming is inconsistent | `screens/intro_screen.py` vs `start_screen.py`, `settings_screen.py` | It is less obvious that `intro_screen.py` is a screen module | Rename to `screens/intro_screen.py` | Sí |
| Asset names mix styles | `sevilla_ganador.png`, `ss_jamon.png`, `feria_pml.png`, `protestas_metro.png`, `mas_rebujito.png` | Harder to search, reference, and enforce consistency in JSON | Normalize to lowercase snake_case and update JSON references | Sí |
| `core/renderer.py` is too broad | Contains stats rendering, card rendering, final screen, confirmation modal, re-election screen | Rendering changes become risky and merge-prone | Split into card, stats, modal/final-screen renderers | Sí |
| `config.py` is not just config | Initializes Pygame display, loads fonts, icons, and JSON | Importing config starts runtime behavior | Split constants/resource paths from runtime initialization | Sí |

### Suggested Improved Structure

```text
Sevilla-Reigns-Game/
  README.md
  REPOSITORY_AUDIT.md
  requirements.txt
  pyproject.toml
  .gitignore
  LICENSE

  main.py
  config/
    __init__.py
    settings.py
    paths.py

  core/
    __init__.py
    event.py
    event_manager.py
    effects.py
    game_state.py

  rendering/
    __init__.py
    card_renderer.py
    stats_renderer.py
    modal_renderer.py
    transition.py

  screens/
    __init__.py
    start_screen.py
    intro_screen.py
    modal_screens.py
    tutorial_screen.py
    settings_screen.py
    credits_screen.py

  ui/
    __init__.py
    button.py

  audio/
    __init__.py
    sounds.py

  data/
    eventos.json
    motivos_muerte.json
    event_schema.json

  resources/
    fonts/
    images/
    sounds/

  tests/
    test_event_manager.py
    test_effects.py
    test_data_integrity.py

  scripts/
    validate_data.py

  docs/
    data_format.md
    architecture.md
```

This structure is intentionally modest. A full `src/` layout would be more professional for packaging, but the above keeps the current project recognizable while improving maintainability.

## 3. Architecture Review

### Entry Point Design

Status: Resuelto.

`main.py` is now a thin executable entry point. It calls `initialize_pygame()`, creates `GameApp`, runs it, and then calls `pygame.quit()`. Runtime startup remains guarded by `if __name__ == "__main__": main()`.

What changed:

- `app.py` now owns application coordination through `GameApp`.
- `runtime.py` owns Pygame initialization.
- `main.py` no longer contains screen routing or the game loop.
- `python -c "import main; import app"` imports safely without starting the game loop.

Remaining note:

- Importing `app.py` still imports `pygame`, which prints the Pygame banner. This is acceptable for now because it does not open a display or start gameplay.

### Main Game Loop

Status: Parcialmente resuelto.

The old `bucle_del_juego` function was removed from `main.py`. `GameApp.run_game_loop()` now owns the frame loop, while supporting responsibilities were extracted:

- `core/game_session.py`: starts a run, resets stats, tracks current event, tracks cards played, and handles the re-election threshold.
- `core/decision_resolver.py`: applies the selected option and delegates stat mutation to `core/effects.py`.
- `app.py`: handles Pygame input polling, swipe animation, screen transitions, and end-state routing.

What improved:

- The core session rules can now be unit tested without Pygame.
- `tests/test_game_session.py` covers stat reset, event-manager progress reset, and the re-election counter.
- Decision application remains single-shot during swipe input.

Remaining risk:

- `GameApp.run_game_loop()` is still a long Pygame loop and is not unit tested directly. That is acceptable for this project size, but future work should move more frame/update logic into smaller pure functions if mechanics grow.

### Screen Routing and Navigation

Status: Resuelto.

Routes are now centralized in `screens/routes.py`:

```python
MENU = "menu"
GAME = "game"
SETTINGS = "settings"
TUTORIAL = "tutorial"
CREDITS = "credits"
QUIT = "quit"
```

What changed:

- `GameApp` uses `screens.routes` instead of duplicated string literals.
- `screens/start_screen.py`, `screens/tutorial_screen.py`, `screens/settings_screen.py`, and `screens/credits_screen.py` return route constants.
- The menu exit action now returns `routes.QUIT` instead of calling `sys.exit()` directly.

What changed after the code-quality refactor:

- `core/transition.py` now returns `routes.QUIT` instead of calling `pygame.quit()` / `sys.exit()`.
- Modal/final/re-election loops were moved into `screens/modal_screens.py`.
- `rendering/modal_renderer.py` is now only a compatibility re-export module.

### State Management

Status: Resuelto.

What is good:

- The stats are centralized.
- Effects clamp values to `0..100`.
- `GameSession` now owns per-run flow state: current event, cards played, and explicit `GameState`.
- `EventManager.reset_progress()` resets unlocked/activated event progress at new-game boundaries.

What changed:

- `main.py` no longer resets stats directly.
- `GameSession.start()` resets `GameState` and event-manager progress intentionally.
- Starting a new game from the menu no longer inherits previous activated/unlocked event state.

What changed after the code-quality refactor:

- `core/game_state.py` now exposes a `GameState` dataclass instead of a global mutable `stats` dictionary.
- `core/effects.py` receives `GameState` explicitly.
- `rendering/stats_renderer.py` receives `GameState` explicitly.
- Tests create isolated `GameState` instances, so core tests are no longer order-dependent on global stats.

### Rendering Responsibilities

Status: Resuelto.

Rendering responsibilities were split into focused modules:

- `rendering/card_renderer.py`: event card drawing, wrapped text, cached event images.
- `rendering/stats_renderer.py`: stat bar/icon rendering.
- `screens/modal_screens.py`: final screen, exit confirmation, and re-election screen loops.
- `rendering/modal_renderer.py`: compatibility shim that re-exports modal screen functions.
- `core/renderer.py`: compatibility shim that re-exports rendering/screen functions.

What improved:

- Card rendering changes no longer touch stat rendering.
- The previous per-frame event image loading/scaling issue was fixed with image caches in `rendering/card_renderer.py`.
- `GameApp` imports rendering modules directly instead of relying on the broad `core.renderer` module.
- Blocking modal loops are no longer in a rendering module.

### Configuration and Resource Loading

Status: Resuelto para import-time side effects.

`config.py` now contains constants, resource paths, and runtime placeholders only. It no longer calls `pygame.init()`, opens a display, loads fonts/icons, or reads JSON on import.

What changed:

- `runtime.py` provides `initialize_pygame()`.
- Font/icon/display initialization happens during app startup.
- Domain tests can import core modules without opening a fullscreen display.
- `config.DATA_PATH`, `config.IMG_PATH`, and other paths are derived from the repository location rather than the current working directory.

Remaining risk:

- `config.py` is still a single module rather than a `config/` package with `settings.py` and `paths.py`. That split is optional at the current project size.
- Missing fonts/icons still fail during startup rather than showing a fallback UI.

### Data Loading

Status: Parcialmente resuelto.

What is good:

- Game content is data-driven.
- Current JSON references are internally consistent.
- `tests/test_data_integrity.py` validates event IDs, option counts, stat names, unlock/requirement references, death reasons, and image paths.
- `scripts/validate_data.py` provides a CLI validation check for the same content class before gameplay or CI.

Remaining risk:

- `core/event_manager.py` still loads raw JSON directly and assumes constructor-compatible event records.
- There is still no `event_schema.json` for editor/tooling validation.

Next improvement:

- Add a formal JSON schema if content editing becomes frequent or non-developers edit `data/eventos.json`.

## 4. Code Quality and Maintainability

| Issue | Where | Problem | Consequence | Improvement | Resuelto |
| --- | --- | --- | --- | --- | --- |
| Top-level runtime loop | `main.py` | Game started on import before the refactor | Could not safely import for tests | Wrapped startup in `main()` and moved coordination to `GameApp` | Sí |
| Import side effects | `config.py` | Initialized Pygame and created fullscreen display on import | Tests and CI were brittle | Runtime init moved to `runtime.initialize_pygame()` | Sí |
| Oversized renderer | `core/renderer.py` | Multiple responsibilities in one file | UI changes were harder to isolate | Split card/stats/modal rendering into focused modules | Sí |
| Magic numbers | `app.py`, `rendering/*`, `screens/*`, `core/transition.py` | Layout/game tuning values were inline | Tuning layout/game rules required hunting through code | Moved repeated layout/game values to named module constants | Sí |
| Global mutable state | `core/game_state.py`, `core/effects.py` | `stats` was mutated from global module state | Hidden dependencies and harder tests | Introduced explicit `GameState` passed through session/effects/rendering | Sí |
| Broad exception handling | `rendering/card_renderer.py`, `core/transition.py` | `except Exception` hid specific failures | Missing/corrupt assets could be silently ignored | Catch concrete file/Pygame errors and render fallback surfaces | Sí |
| No type hints | Core domain modules | Function contracts were implicit | Harder onboarding and refactoring | Added type hints to `GameState`, `Event`, `EventManager`, effects, session, and transition seams | Sí |
| Mixed language/naming | Core APIs and screen/modal functions | Spanish and English identifiers were mixed | Harder for external contributors | Standardized touched internal APIs to English; player-facing text remains Spanish | Sí |
| Dead/unused imports | Screens, rendering, transition | Some imports were broader than needed | Noise and possible side effects | Removed unused `sys`, global `stats`, old modal imports, and stale code paths | Sí |
| Blocking UI loops in renderer | `rendering/modal_renderer.py` | Modal renderer owned event polling and navigation | Hard to reuse and test | Moved modal/final/re-election loops to `screens/modal_screens.py` | Sí |

Positive notes:

- `core/event.py` is small and readable.
- `core/effects.py` centralizes stat mutation and death reason lookup.
- `EventManager` now avoids recursive selection failure and uses IDs for activated events.
- `GameApp` now centralizes application coordination outside `main.py`.
- `GameSession` owns an explicit `GameState`, making per-run state easier to test.
- `screens/routes.py` removes duplicated route strings.
- `screens/modal_screens.py` keeps blocking screen loops out of rendering modules.
- `requirements.txt` pins the observed Pygame version.

## 5. Functionality and Game Logic

### Core Game Flow

The flow is:

1. Start menu.
2. Game intro card.
3. Select event from `EventManager`.
4. Player presses left/right.
5. Apply option effects.
6. Animate card off-screen.
7. Check stat death condition.
8. Every 30 cards, show re-election and reset stats.
9. Continue with next event.

This is clear enough for a small game. The rules are now split across `app.py`, `core/game_session.py`, `core/decision_resolver.py`, `core/event_manager.py`, `core/effects.py`, and `core/game_state.py`. `GameState` is explicit and owned by `GameSession`, so the game-rule flow is no longer tied to a global `stats` dictionary.

### Event Selection

`EventManager` uses:

- `eventos_disponibles`
- `eventos_activados`
- `eventos_desbloqueados`
- `requisitos`
- `desbloquea`

Current data integrity check:

- 31 events.
- No duplicate IDs.
- No bad requirement references.
- No bad unlock references.
- Every event has exactly two options.
- All stat keys are valid.
- All events are statically reachable.

Status:

- Event unlocking depends on choosing the option that unlocks follow-up events. This is intentional and documented in `docs/data_format.md`.
- If the player never chooses an unlocking option, follow-up events stay unavailable for that session.
- `EventManager` progress is now reset by `GameSession.start()` through `EventManager.reset_progress()`, so a new run starts with fresh activated/unlocked event state.

Implemented:

- Unlock state is documented as session-scoped.
- Requirement/unlock behavior is covered by `tests/test_event_manager.py`.

### Stat Changes and End Conditions

`GameState.apply_effects()` clamps stats to `0..100`, and `get_end_stat(game_state)` returns the first stat at either boundary.

Status:

- If multiple stats cross a boundary in one decision, the game now uses the documented priority in `core.game_state.END_STAT_PRIORITY`.
- Priority is documented in `docs/data_format.md`.

Implemented:

- `tests/test_effects.py` verifies the multi-stat end priority.

### Death/Failure Reasons

`data/motivos_muerte.json` maps stat + zero/hundred to text and image.

What is good:

- Death reasons are data-driven.
- All referenced death images exist.

Risk:

- If a stat is added later, death reasons must be updated manually.
- Missing keys fall back to generic messages, which avoids crashes but can hide data gaps.

Implemented:

- `tests/test_data_integrity.py` validates that every stat has `zero` and `hundred` reasons and that all referenced death images exist.

### Screen Transitions

`core/transition.py` provides a custom tile transition. This is a good portfolio detail.

Status:

- Transition resolves `azulejo.jpg` through `config.IMG_PATH`.
- It now returns `routes.QUIT` on quit events instead of exiting the process internally.

Implemented:

- Asset path and quit-signal recommendations are implemented in `core/transition.py`.

### Button Interactions

`ui/button.py` is simple and clear. It handles hover and click sound.

Status:

- Mouse activation works.
- Keyboard focus, Enter, and Space activation are implemented in `ui/button.py`.
- The start menu supports arrow/tab navigation.
- No disabled state.
- No visual pressed state.

Remaining polish:

- Add visual pressed state only if menu polish becomes a priority.

### Save/Load Behavior

No disk save/load behavior exists. That is acceptable for a small arcade-style game. Runtime settings now persist in memory through `SettingsState`, so music/effects volume no longer resets when revisiting the settings screen. If the game becomes longer or progression matters, add a save file for unlocked events and settings.

## 6. Data and Content Audit

### Data Files

| File | Purpose | Health |
| --- | --- | --- |
| `data/eventos.json` | Event/card content | Valid JSON, 31 events, references valid, all images exist |
| `data/motivos_muerte.json` | Death/failure messages and images | Valid JSON, all referenced images exist |

### Current Data Findings

- No missing image references.
- No unused images by current code/JSON reference scan.
- No unused sounds by current code reference scan.
- No duplicate event IDs.
- No invalid option counts.
- No invalid stat keys.
- No bad unlock/requirement references.
- All events are reachable under the static unlock graph.

### Status

- `scripts/validate_data.py` and `tests/test_data_integrity.py` catch broken IDs, options, stat names, references, death reasons, and missing images.
- The event format is now documented in `docs/data_format.md`.
- `image`, `requisitos`, and `desbloquea` are documented optional fields.
- Text style is inconsistent: some Spanish text lacks accents (`Si`, `futbol`, `publicas`, `prohibicion`), while other entries use accents correctly.
- Stat names are internal English terms, and the player-facing mapping is documented in `docs/data_format.md` and rendered below the stat icons.

### Remaining Recommendation

- Add a formal `event_schema.json` only if content editing becomes frequent.
- Normalize remaining Spanish content style and accents as a content polish pass.
- Run `scripts/validate_data.py` in CI once CI exists.

## 7. UI/UX Review

### What Works

- The core interaction is simple: left/right decisions.
- The game has a strong theme and personality.
- Fullscreen mode gives an arcade/presentation feel.
- Custom assets, fonts, sounds, and tile transition make the project more memorable than a plain Pygame demo.

### Specific UI Problems

| Problem | Where | Impact | Recommendation |
| --- | --- | --- | --- |
| Stats were icon-only | `rendering/stats_renderer.py` | New players may not understand what each icon means | Resolved: labels are rendered below icons |
| Consequence feedback was hidden | `app.py`, `rendering/stats_renderer.py` | Player saw stats move only indirectly | Resolved: last decision deltas are shown near stat icons |
| Layout uses fixed pixel assumptions | `rendering/*`, `screens/*.py` | Text/buttons may not scale perfectly across ultrawide/small displays | Improved with named constants; responsive layout pass remains future polish |
| Card description position depended on image assumptions | `rendering/card_renderer.py` | Descriptions could be too low/high depending on asset aspect ratio | Improved: description starts after actual scaled image height |
| Text wrapping did not limit vertical overflow | `draw_text_wrapped` | Long descriptions/options could overlap buttons or leave the card | Resolved for wrapped text: overflow is truncated with suffix |
| Buttons are visually basic | `ui/button.py` | Menu looks prototype-level | Add consistent colors, padding, hover/pressed states, and font hierarchy |
| No keyboard menu navigation | `screens/start_screen.py`, `ui/button.py` | Full keyboard flow was incomplete | Resolved: arrow/tab focus plus Enter/Space activation |
| Fullscreen only | `main.py`, `runtime.py` | Inconvenient for development and some users | Resolved for development: run `python main.py --windowed` |
| Settings reset every visit | `screens/settings_screen.py`, `core/settings_state.py` | User changes were not persistent within app navigation | Resolved in memory through `SettingsState` |

### Portfolio Polish Suggestions

- Add a screenshot/GIF to `README.md`.
- Add a polished title screen layout with clearer visual hierarchy.
- Further polish stat delta animation: pulse icons green/red rather than only showing numeric deltas.
- Add a small "year" or "mandate" counter to reinforce progression.
- Make menu, tutorial, credits, and settings screens share a common screen layout helper.

## 8. Assets and Visual Design

### Current Asset Health

| Asset Type | Count | Findings |
| --- | ---: | --- |
| Images | 52 | All referenced; no missing or unused images found by static scan |
| Sounds | 6 | All referenced; no unused sounds found by static scan |
| Fonts | 2 | `andalus.ttf` is used; `Sevillana-Regular.ttf` appears present for style but not referenced by current code |

### Concerns

- Several PNGs are large: `cruzcampo_bancarrota.png` is about 3.9 MB; many others are above 3 MB.
- `draw_event` loads and scales the event image every frame. This is the most important performance issue in the repo.
- Asset paths are often hardcoded relative strings: `"resources/images/..."`.
- Naming style is inconsistent across assets.
- There is no manifest or asset loader.

### Recommendations

- Preload event images once per event or cache scaled surfaces by `(image_name, max_size)`.
- Normalize filenames to lowercase snake_case.
- Add a path helper module so resource loading does not depend on the current working directory.
- Consider compressing large PNGs or using optimized formats where appropriate.
- Add fallback surfaces for missing/corrupt event images, not just `print`.

## 9. Testing and Quality Assurance

### Current Testing Situation

Tests now exist for the core game rules and data integrity. This area is no longer empty, but UI/frame-loop behavior is still mostly covered by manual QA.

### What Is Currently Testable

- `core/event_manager.py` can be tested without Pygame.
- `core/effects.py` can be tested with isolated `GameState` instances.
- JSON data can be validated without Pygame.
- `core/event.py` constructors can be tested.

### What Is Hard to Test

- `GameApp.run_game_loop()`, because it depends on real Pygame event polling and frame rendering.
- Pygame screen loops in `screens/modal_screens.py`, because they intentionally block while waiting for user input.
- Pygame rendering modules generally require initialized fonts/icons from runtime startup.

### Recommended Test Structure

```text
tests/
  conftest.py
  test_event_manager.py
  test_effects.py
  test_data_integrity.py
  test_death_reasons.py
```

### First Tests to Add

| Test File | What To Verify |
| --- | --- |
| `tests/test_event_manager.py` | Repeated selection does not recurse/crash; requirements block events until unlocked; `desbloquea` works for string/list |
| `tests/test_effects.py` | Effects apply correctly; stats clamp to `0..100`; unknown stats do not mutate state |
| `tests/test_data_integrity.py` | JSON parses; event IDs unique; exactly two options per event; valid stat names; valid image paths; valid requirement/unlock references |
| `tests/test_death_reasons.py` | Every stat has zero/hundred reasons; every referenced death image exists |

### Avoiding Pygame Initialization in Tests

- Prefer core tests that do not initialize Pygame.
- Keep Pygame setup in explicit startup functions.
- Keep data/domain tests focused on `core.event`, `core.event_manager`, and `core.effects`.
- If Pygame tests are needed, use `SDL_VIDEODRIVER=dummy` in CI.

### Manual QA Checklist

- Start game from clean checkout.
- Navigate menu buttons with mouse.
- Start game and choose left/right.
- Confirm stats change once per decision.
- Trigger death at `0` and `100`.
- Reach re-election after 30 cards.
- Open settings and change music/effects volume.
- Escape from game and confirm/cancel exit.
- Confirm all event images render.
- Run at multiple resolutions/window modes once supported.

## 10. Dependency and Tooling Review

### Current State

- `requirements.txt` exists with `pygame==2.6.1`.
- `.gitignore` exists and covers Python bytecode, virtualenvs, and common caches.
- No `pyproject.toml`.
- No test dependency.
- No formatter/linter/type checker config.
- No CI workflow.

### Minimal Tooling Setup

Appropriate if the project stays small:

```text
requirements.txt
requirements-dev.txt
.gitignore
tests/
```

`requirements-dev.txt`:

```text
pytest
ruff
```

### Professional Tooling Setup

Appropriate if this is a portfolio project:

```text
pyproject.toml
requirements.txt
tests/
.github/workflows/ci.yml
```

Recommended tools:

- `ruff` for linting and formatting.
- `pytest` for tests.
- Optional `mypy` after type hints are added.

### Recommendation

Use the professional setup. This is small overhead and improves recruiter confidence. A simple GitHub Actions workflow running `python -m compileall .`, `python -m json.tool`, `pytest`, and `ruff check` would be enough.

## 11. Error Handling and Robustness

### Runtime Crash Risks

| Risk | Where | Why It Matters | Safeguard |
| --- | --- | --- | --- |
| Missing font crashes at import | `config.py:23` | App cannot start and error is not user-friendly | Load fonts in startup with fallback to default font |
| Missing icon crashes at import | `config.py:32` | Any import of config can fail | Add asset loader validation and fallback surface |
| Missing music/sound crashes at import/load | `core/sounds.py` | Audio files are assumed present | Catch `pygame.error`, allow muted mode |
| Invalid event JSON crashes startup | `core/event_manager.py` | No schema validation | Validate data before creating `Event` objects |
| Empty events list returns `None` | `EventManager` | Main handles this partly, but UX is a death screen | Show a content error screen/log, not "mocion de censura" |
| Relative paths depend on cwd | Multiple modules | Running from another directory can fail | Use `Path(__file__).resolve()` based project root |
| Fullscreen may fail/headless env | `main.py`, `runtime.py` | CI/dev environments may not support display | Windowed startup is available with `python main.py --windowed`; use dummy SDL driver for automated Pygame tests |

### Concrete Safeguards

- Add `validate_data.py`.
- Add `ResourceLoader` with explicit error messages.
- Add fallback fonts/images/sounds.
- Use `python main.py --windowed` during development/demo when fullscreen is inconvenient.
- Continue returning quit signals to the app loop instead of exiting inside helper modules.

## 12. Performance Review

The project is small enough that performance is not a major issue, but there is one real problem.

### Important Issue: Per-frame Image Loading

The original `core/renderer.py` loaded and scaled event images every frame in `draw_event`; this has been fixed in `rendering/card_renderer.py` with image caches.

Consequence:

- Disk I/O and image scaling happen 60 times per second.
- Large PNGs above 3 MB make this unnecessarily expensive.
- The game may stutter on slower machines.

Recommendation:

- Load each event image once when the event is selected.
- Cache original surfaces by filename.
- Cache scaled surfaces by target dimensions.

### Other Observations

- Font objects are loaded once, which is good.
- Icon images are loaded once, which is good.
- JSON files are loaded once per manager/module, which is fine for this size.
- `draw_stats` scales icons every frame; cache scaled stat icons for current `icon_size`.
- Transition tiles are loaded each transition; acceptable, but can be cached.

## 13. Portfolio and Recruiter Readiness

### Current Portfolio Assessment

The idea is strong: a localized Reigns-style game with custom content, humor, sounds, and generated imagery. That is memorable. The repository presentation, however, does not yet show professional engineering discipline.

### What Holds It Back

- README lacks setup/run instructions.
- No screenshots or GIF.
- No tests.
- No architecture explanation.
- No CI.
- Code starts runtime loops on import.
- Rendering and configuration are tightly coupled.
- Asset/content format is undocumented.

### Improvements That Would Impress Recruiters

- Add a demo GIF and screenshots to README.
- Add "How to run" and "How to test" sections.
- Add data validation tests to prove JSON-driven content is safe.
- Add a short `docs/architecture.md` explaining the game loop, event data, and screen flow.
- Add CI badge after GitHub Actions is configured.
- Split rendering/configuration enough that the structure looks intentional.

## 14. Documentation Review

### Current README

`README.md` exists and explains the game concept and controls at a high level. It is too short for a project meant to be shared.

Missing README sections:

- Requirements: Python version and Pygame.
- Installation.
- Run command.
- Controls.
- Game rules.
- Screenshots/demo.
- Project structure.
- Testing.
- Credits/licensing for generated assets and fonts.

### Documentation to Add

| File | Purpose |
| --- | --- |
| `docs/architecture.md` | Explain app startup, screen routing, game loop, event manager, stats/effects |
| `docs/data_format.md` | Document event JSON schema, valid stats, unlocks, image references |
| `docs/assets.md` | Asset naming, expected image sizes, compression, sound format |
| `CONTRIBUTING.md` | Optional; useful if project is public or collaborative |
| `LICENSE` | Needed if shared publicly |

## 15. Security and Safety Review

This is a local game with no network surface and no credentials. Security risk is low.

Minor concerns:

- JSON and asset paths are trusted local input.
- Relative paths can load from an unexpected working directory if the game is launched incorrectly.
- No sensitive values are present.
- Dependency footprint is small: only Pygame.

Recommendations:

- Resolve paths from the repository/module root.
- Keep dependencies pinned.
- Do not load arbitrary user-supplied paths without validation if modding is added later.

## 16. Prioritized Action Plan

### Priority 1 — Critical / High Impact

| Task | Why It Matters | Files Affected | Estimated Difficulty | Resuelto |
| --- | --- | --- | --- | --- |
| Move runtime startup out of imports | Enables tests, CI, and safe imports | `main.py`, `config.py` | Medium | Sí |
| Add data validation tests | Prevents broken JSON/assets from crashing the game | `tests/test_data_integrity.py`, `data/*.json` | Low | Sí |
| Add unit tests for event/effects logic | Protects core game rules from regressions | `tests/test_event_manager.py`, `tests/test_effects.py`, `core/*` | Low | Sí |
| Stop loading/scaling event images every frame | Prevents stutter and wasted I/O | `core/renderer.py`, possible asset loader | Medium | Sí |
| Document setup/run instructions | Makes the repo runnable by reviewers/recruiters | `README.md` | Low | Sí |

### Priority 2 — Important / Medium Impact

| Task | Why It Matters | Files Affected | Estimated Difficulty | Resuelto |
| --- | --- | --- | --- | --- |
| Split `core/renderer.py` | Reduces coupling and makes UI changes safer | `core/renderer.py`, `rendering/*` | Medium | Sí |
| Add package markers | Improves import clarity and test discovery | `core/__init__.py`, `screens/__init__.py`, `ui/__init__.py` | Low | Sí |
| Rename `event_manager.py` | Aligns with Python naming conventions | `core/event_manager.py`, imports | Low | Sí |
| Rename `intro_screen.py` | Makes screen module naming consistent | `screens/intro_screen.py`, imports | Low | Sí |
| Add centralized routes | Prevents mistyped navigation strings | `screens/routes.py`, `app.py`, `screens/*` | Low | Sí |
| Add app/session coordinator split | Makes startup and game-loop responsibilities clearer | `app.py`, `core/game_session.py`, `core/decision_resolver.py` | Medium | Sí |
| Add data validation script | Lets CI/reviewers validate JSON/assets without running the game | `scripts/validate_data.py` | Low | Sí |
| Add `pyproject.toml` with Ruff/Pytest config | Professionalizes workflow | `pyproject.toml` | Low | No |
| Add CI workflow | Shows engineering discipline and catches regressions | `.github/workflows/ci.yml` | Low | No |
| Add windowed/dev mode | Improves development and demo usability | `main.py`, `runtime.py` | Medium | Sí |

### Priority 3 — Polish / Nice to Have

| Task | Why It Matters | Files Affected | Estimated Difficulty |
| --- | --- | --- | --- |
| Normalize asset filenames | Improves searchability and consistency | `resources/images/*`, `data/eventos.json`, `data/motivos_muerte.json` | Medium |
| Add stat labels and delta feedback | Makes gameplay clearer | `rendering/stats_renderer.py`, `app.py` | Medium | Sí |
| Add README screenshots/GIF | Improves recruiter presentation | `README.md`, `docs/` or `resources/` | Low |
| Add keyboard menu navigation | Improves accessibility and polish | `ui/button.py`, `screens/start_screen.py` | Medium | Sí |
| Compress large PNGs | Reduces repo size and load time | `resources/images/*.png` | Low |
| Add `LICENSE` | Clarifies reuse rights | `LICENSE` | Low |

## 17. Suggested Final Repository Structure

Recommended target structure without unnecessary complexity:

```text
Sevilla-Reigns-Game/
  README.md
  REPOSITORY_AUDIT.md
  LICENSE
  requirements.txt
  requirements-dev.txt
  pyproject.toml
  .gitignore

  main.py
  app.py
  runtime.py

  config/
    __init__.py
    paths.py
    settings.py

  core/
    __init__.py
    decision_resolver.py
    event.py
    event_manager.py
    effects.py
    game_session.py
    game_state.py

  rendering/
    __init__.py
    card_renderer.py
    stats_renderer.py
    modal_renderer.py
    transition.py

  screens/
    __init__.py
    routes.py
    start_screen.py
    intro_screen.py
    modal_screens.py
    tutorial_screen.py
    settings_screen.py
    credits_screen.py

  ui/
    __init__.py
    button.py

  audio/
    __init__.py
    sounds.py

  data/
    eventos.json
    motivos_muerte.json
    event_schema.json

  resources/
    fonts/
    images/
    sounds/

  tests/
    conftest.py
    test_event_manager.py
    test_effects.py
    test_data_integrity.py
    test_death_reasons.py

  scripts/
    validate_data.py

  docs/
    architecture.md
    data_format.md
    assets.md

  .github/
    workflows/
      ci.yml
```

## 18. Final Verdict

| Score | Rating |
| --- | ---: |
| Overall | 6/10 |
| Architecture | 7/10 |
| Code quality | 7/10 |
| Testing | 6/10 |
| UI/UX | 6/10 |
| Portfolio readiness | 6/10 |

### The 5 Most Important Next Actions

1. Add `pyproject.toml`, Ruff/Pytest config, and a simple GitHub Actions CI workflow.
2. Add fallback handling for missing/corrupt fonts and sounds.
3. Add optional Pygame smoke tests using `SDL_VIDEODRIVER=dummy`.
4. Improve README with screenshots/GIF and a short architecture/data-format section.
5. Document the English-in-code, Spanish-in-player-text naming convention.

The project has a strong concept and enough custom content to be interesting. The next level is engineering maturity: explicit startup, testable core logic, documented data formats, and a cleaner rendering/resource-loading boundary.
