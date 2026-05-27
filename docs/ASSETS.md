# Assets

## Menu icons

The original static menu icons used by the Pygame home screen are external assets from [Game-icons.net](https://game-icons.net/), downloaded from the official [game-icons/icons GitHub repository](https://github.com/game-icons/icons).

License: [Creative Commons Attribution 3.0 Unported](https://creativecommons.org/licenses/by/3.0/). Attribution is required.

The original downloaded menu SVGs are not required at runtime because the generated animated frames and static fallbacks are committed.

| Button | Asset | Author | Source |
| --- | --- | --- | --- |
| Comenzar | `entry-door.svg` | Delapouite | https://game-icons.net/1x1/delapouite/entry-door.html |
| Tutorial | `open-book.svg` | Lorc | https://game-icons.net/1x1/lorc/open-book.html |
| Ajustes | `gears.svg` | Lorc | https://game-icons.net/1x1/lorc/gears.html |
| Creditos | `flower-emblem.svg` | Delapouite | https://game-icons.net/1x1/delapouite/flower-emblem.html |
| Salir | `exit-door.svg` | Delapouite | https://game-icons.net/1x1/delapouite/exit-door.html |

The icons were recolored to match the project palette: cobalt blue for standard buttons and ivory for the burgundy exit button. The home screen uses generated animated frames first, then `resources/icons/static/` as the only menu fallback.

## Animated menu icons

The home screen hover icons are PNG frame sequences generated locally with `scripts/generate_animated_menu_icons.py`. They use transparent 64x64 canvases, fixed alignment, and the existing palette: cobalt blue, albero gold, and ivory.

Searches were checked for external animated icons and spritesheets, including Lottie/GIF/spritesheet sources such as LottieFiles-style gear/book/door searches and Pixabay book page flip GIF results. No downloaded animated asset was used because the available results either did not match the Sevilla premium style closely enough, added licensing/attribution friction, or would require a heavier conversion workflow than needed for Pygame.

| Button | Asset name | Location | Source | Author | License | Link | Modifications | PNG frames |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Comenzar | `comenzar` animated arch door | `resources/icons/animated/comenzar/frame_00.png` to `frame_15.png` | Custom vector composition generated in this repository; concept aligned with the existing `entry-door.svg` menu icon | OpenAI Codex for this project | Project asset, generated for this repository | `scripts/generate_animated_menu_icons.py` | Door panel opens internally and warm albero light appears inside a fixed arch; 64x64 transparent frames | Yes |
| Tutorial | `tutorial` animated open book | `resources/icons/animated/tutorial/frame_00.png` to `frame_15.png` | Custom vector composition generated in this repository; concept aligned with the existing `open-book.svg` menu icon | OpenAI Codex for this project | Project asset, generated for this repository | `scripts/generate_animated_menu_icons.py` | Page polygon flips over a static open book; 64x64 transparent frames | Yes |
| Ajustes | `ajustes` animated gears | `resources/icons/animated/ajustes/frame_00.png` to `frame_15.png` | Custom vector composition generated in this repository; concept aligned with the existing `gears.svg` menu icon | OpenAI Codex for this project | Project asset, generated for this repository | `scripts/generate_animated_menu_icons.py` | Two independent gear shapes rotate in opposite directions; 64x64 transparent frames | Yes |
| Creditos | `creditos` animated flower medal | `resources/icons/animated/creditos/frame_00.png` to `frame_15.png` | Custom vector composition generated in this repository; concept aligned with the existing `flower-emblem.svg` menu icon | OpenAI Codex for this project | Project asset, generated for this repository | `scripts/generate_animated_menu_icons.py` | Ornamental flower/medal stays fixed while a small sparkle travels around it; 64x64 transparent frames | Yes |
| Salir | `salir` animated exit door | `resources/icons/animated/salir/frame_00.png` to `frame_15.png` | Custom vector composition generated in this repository; concept aligned with the existing `exit-door.svg` menu icon | OpenAI Codex for this project | Project asset, generated for this repository | `scripts/generate_animated_menu_icons.py` | Door opens internally and the gold exit arrow extends outward inside a fixed canvas; 64x64 transparent frames | Yes |

Static first-frame PNGs are stored in `resources/icons/static/` and are the fallback used when an animated frame sequence cannot be loaded.

## Election victory intro emblem

The pre-game victory screen uses a local NO8DO emblem generated with `scripts/prepare_intro_assets.py` and saved as `resources/icons/pygame/intro/no8do_emblem.png`. Its visual reference is the public-domain Sevilla emblem from Wikimedia Commons.

| Screen | Asset | Author | Source | License | Link | Modifications |
| --- | --- | --- | --- | --- | --- | --- |
| Intro victory | `no8do_emblem.png` | Generated for this project | Wikimedia Commons visual reference | Public domain reference | https://commons.wikimedia.org/wiki/File:Emblema_de_sevilla.svg | Rendered locally as `NO8DO` text with the project palette and typography; exported as a transparent Pygame-ready PNG. |

The confetti on the victory screen is implemented as lightweight Pygame particles rather than a downloaded animation asset. It uses only the project palette and is drawn behind the central panel so it reinforces the celebration without covering the text.

## Event category icons

The event decision screen category bar uses restored legacy azulejo symbols from the original stat icons. The Pygame-ready files in `resources/icons/categories/` are transparent crops of the central symbol so the current vertical fill animation can use their alpha masks cleanly.

| Category | Asset | Source | Modifications |
| --- | --- | --- | --- |
| Tradición | `cross_cobalt.png` | `resources/images/religion_sil.png` | Cropped to the central cross and exported on a transparent square canvas. |
| Vecindario | `flamenca_cobalt.png` | `resources/images/people_sil.png` | Cropped to the flamenca silhouette, removed small frame artifacts, and exported on a transparent square canvas. |
| Dinero | `euro_cobalt.png` | `resources/images/money_sil.png` | Cropped to the central euro symbol and exported on a transparent square canvas. |
| Turismo | `suitcases_cobalt.png` | `resources/images/tourism_sil.png` | Cropped to the central suitcase group and exported on a transparent square canvas. |

The event image for `Cambio de recorrido` already exists in `resources/images/cambio_de_recorrido.png`, so no new event illustration was added for this screen.

## UI fonts

The game UI uses local font files downloaded from the official [Google Fonts repository](https://github.com/google/fonts), so rendering does not depend on system-installed fonts.

License: [SIL Open Font License 1.1](https://openfontlicense.org/). Local license copies are stored as `resources/fonts/Cinzel-OFL.txt` and `resources/fonts/CormorantGaramond-OFL.txt`.

| Font | Author / Foundry | Source | License | Local files | Usage |
| --- | --- | --- | --- | --- | --- |
| Cinzel | Natanael Gama | Google Fonts | SIL OFL 1.1 | `Cinzel-Regular.ttf`, `Cinzel-SemiBold.ttf`, `Cinzel-Bold.ttf` | Main title, event titles, category labels, buttons, important headings. |
| Cormorant Garamond | Christian Thalmann / Catharsis Fonts | Google Fonts | SIL OFL 1.1 | `CormorantGaramond-Regular.ttf`, `CormorantGaramond-Medium.ttf`, `CormorantGaramond-SemiBold.ttf` | Narrative text, descriptions, subtitles, instructions, credits, tutorial body text. |

Downloads:
- Cinzel: https://fonts.google.com/specimen/Cinzel and https://github.com/google/fonts/tree/main/ofl/cinzel
- Cormorant Garamond: https://fonts.google.com/specimen/Cormorant+Garamond and https://github.com/google/fonts/tree/main/ofl/cormorantgaramond
