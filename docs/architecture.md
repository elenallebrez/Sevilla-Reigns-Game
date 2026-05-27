# Architecture

This project is a Python/Pygame desktop game. It uses a lightweight Clean Architecture layout under `src/sevilla_reigns`.

## Layers

```text
domain/entities/     Pure game entities and state rules.
application/         Game use cases: sessions, decisions, event loading, effects.
infrastructure/      Pygame-facing adapters such as audio and transitions.
presentation/        Screens, rendering modules, and UI components.
config/              Runtime paths, mutable Pygame handles, fonts, and visual theme.
main/                Application coordinator and Pygame startup.
```

## Dependency Direction

- `domain` does not import Pygame or presentation modules.
- `application` may use domain entities and repository-like loaders.
- `infrastructure` owns Pygame-specific services such as sounds and transitions.
- `presentation` owns drawing and screen event loops.
- `main` composes all layers and runs the app.

## Root Folders

- `data/`: JSON game content.
- `assets/`: images, icons, fonts, and sounds.
- `scripts/`: validation and asset generation tools.
- `tests/`: automated checks for data and game rules.
