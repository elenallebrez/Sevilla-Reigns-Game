# Sevilla Reigns

Un juego tipo **Reigns** ambientado en Sevilla, con humor absurdo, referencias modernas y decisiones que pondrán a prueba tu mandato.

¿Conseguirás que el pueblo te reelija o acabarás fuera del Ayuntamiento?

## Requisitos

- Python 3.11 o superior recomendado.
- Pygame 2.6.1.

## Instalación

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Para desarrollo y tests:

```bash
pip install -r requirements-dev.txt
```

## Cómo Ejecutar

```bash
python main.py
```

El juego se abre en pantalla completa. Pulsa `Esc` durante la partida para abrir la confirmación de salida al menú.

## Cómo Jugar

- Toma decisiones eligiendo la opción izquierda o derecha de cada carta.
- Cada decisión afecta a tus stats: tradición, vecindario, dinero y turismo.
- Si alguna stat llega a `0` o `100`, termina tu mandato.
- Cada 30 cartas, el pueblo te reelige y las stats vuelven a su estado inicial.
- El juego es infinito: las cartas pueden repetirse, pero tus decisiones cambian la partida.

## Controles

- `←`: elegir opción izquierda.
- `→`: elegir opción derecha.
- `Esc`: volver al menú desde la partida.
- Ratón: usar botones de menú, ajustes, tutorial, créditos y decisiones.

## Tests

```bash
python -m pytest
```

Los tests cubren integridad de datos JSON, referencias a assets, selección y desbloqueo de eventos, aplicación de efectos sobre stats e imports principales.

## Estructura Del Proyecto

```text
core/       Lógica del juego: eventos, efectos, estado, sesión y transiciones.
data/       Eventos y motivos de derrota en JSON.
docs/       Documentación técnica y formato de datos.
rendering/  Renderizado de cartas, stats y elementos visuales.
resources/  Imágenes, iconos, sonidos y fuentes.
screens/    Pantallas de menú, tutorial, ajustes, intro y créditos.
scripts/    Utilidades de validación y generación de assets.
tests/      Tests automáticos de datos y lógica.
ui/         Componentes básicos de interfaz.
```

## Contenido Y Assets

- Los eventos están definidos en `data/eventos.json`.
- Los motivos de derrota están definidos en `data/motivos_muerte.json`.
- Las imágenes referenciadas por los JSON deben existir en `resources/images/`.
- Los iconos y frames animados están en `resources/icons/`.
- Los sonidos están en `resources/sounds/`.
- Las fuentes locales están en `resources/fonts/`.

## Documentación

- Formato de eventos y datos: `docs/data_format.md`.
- Atribución y origen de assets: `docs/ASSETS.md`.
- Auditoría de estructura, arquitectura y mejoras pendientes: `docs/REPOSITORY_AUDIT.md`.
