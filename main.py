import pygame

import config
from core.effects import aplicar_efectos, check_fin, get_info_muerte
from core.eventmanager import EventManager
from core.game_state import get_default_stats, stats


def main():
    config.initialize_pygame()

    from core.renderer import (
        draw_event,
        draw_stats,
        mostrar_confirmacion_salida,
        mostrar_pantalla_final,
        mostrar_pantalla_reeleccion,
    )
    from core.sounds import page_sound, reproducir_musica
    from core.transition import slide_transition
    from screens.credits_screen import credits_screen
    from screens.intro import mostrar_carta_introductoria
    from screens.settings_screen import settings_screen
    from screens.start_screen import start_screen
    from screens.tutorial_screen import tutorial_screen

    event_manager = EventManager(config.DATA_PATH / "eventos.json")
    background = pygame.image.load(str(config.IMG_PATH / "fondo.png"))
    background = pygame.transform.scale(background, (config.WIDTH, config.HEIGHT))

    def bucle_del_juego(screen):
        stats.clear()
        stats.update(get_default_stats())
        mostrar_carta_introductoria(
            screen,
            config.FONT,
            config.FONT,
            config.WIDTH,
            config.HEIGHT,
            background,
        )
        swipe_speed = int(config.WIDTH / 18)
        evento_actual = event_manager.seleccionar_evento()

        if evento_actual is None:
            texto_final = "No quedan más eventos disponibles. ¡Gracias por jugar!"
            return mostrar_pantalla_final(screen, texto_final, None)

        swipe_offset = 0
        swipe_direction = 0
        cartas_jugadas = 0

        while True:
            config.clock.tick(config.FPS)
            screen.fill((200, 200, 255))

            draw_stats(screen)
            draw_event(screen, evento_actual, swipe_offset)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                if event.type != pygame.KEYDOWN or swipe_direction != 0:
                    continue

                if event.key == pygame.K_LEFT:
                    page_sound.play()
                    lado_elegido = 0
                    swipe_direction = -1
                    cambios = event_manager.aplicar_decision(evento_actual, lado_elegido)
                    aplicar_efectos(cambios)
                elif event.key == pygame.K_RIGHT:
                    page_sound.play()
                    lado_elegido = 1
                    swipe_direction = 1
                    cambios = event_manager.aplicar_decision(evento_actual, lado_elegido)
                    aplicar_efectos(cambios)
                elif event.key == pygame.K_ESCAPE:
                    salir = mostrar_confirmacion_salida(screen)
                    if salir:
                        return "menu"

            if swipe_direction == 0:
                continue

            swipe_offset += swipe_speed * swipe_direction
            if abs(swipe_offset) <= config.WIDTH:
                continue

            causa = check_fin()
            if causa:
                texto_muerte, imagen = get_info_muerte(causa, stats[causa])
                return mostrar_pantalla_final(screen, texto_muerte, imagen)

            cartas_jugadas += 1
            if cartas_jugadas >= 30:
                mostrar_pantalla_reeleccion(screen)
                stats.clear()
                stats.update(get_default_stats())
                cartas_jugadas = 0

            evento_actual = event_manager.seleccionar_evento()
            if evento_actual is None:
                texto_final = "No quedan más eventos disponibles. ¡Gracias por jugar!"
                return mostrar_pantalla_final(screen, texto_final, None)

            swipe_offset = 0
            swipe_direction = 0

    def draw_real_screen(surface, screen_name):
        if screen_name in {"menu", "tutorial", "settings", "credits"}:
            surface.blit(background, (0, 0))
            return

        surface.fill((0, 0, 0))

    current_screen = "menu"
    running = True
    reproducir_musica()

    while running:
        if current_screen == "menu":
            next_screen = start_screen(
                config.screen,
                config.WIDTH,
                config.HEIGHT,
                config.FONT,
                config.SUPER_FONT,
                background,
            )
        elif current_screen == "tutorial":
            next_screen = tutorial_screen(
                config.screen,
                config.WIDTH,
                config.HEIGHT,
                config.FONT,
                background,
            )
        elif current_screen == "game":
            next_screen = bucle_del_juego(config.screen)
        elif current_screen == "settings":
            next_screen = settings_screen(
                config.screen,
                config.WIDTH,
                config.HEIGHT,
                config.FONT,
                background,
            )
        elif current_screen == "credits":
            next_screen = credits_screen(
                config.screen,
                config.WIDTH,
                config.HEIGHT,
                config.FONT,
                background,
            )
        elif current_screen == "quit":
            break
        else:
            next_screen = "menu"

        if next_screen == "quit":
            running = False
            break

        if next_screen is None or next_screen == current_screen:
            current_screen = next_screen or current_screen
            continue

        pantalla_actual = config.screen.copy()
        pantalla_siguiente_surface = pygame.Surface((config.WIDTH, config.HEIGHT))
        draw_real_screen(pantalla_siguiente_surface, next_screen)
        pantalla_siguiente = pantalla_siguiente_surface.copy()

        slide_transition(
            config.screen,
            config.clock,
            next_screen,
            tile_size=150,
            fps=60,
            tiles_per_step=6,
            draw_screen_func=lambda surf, name: (
                surf.blit(
                    pantalla_siguiente if name == next_screen else pantalla_actual,
                    (0, 0),
                )
            ),
        )

        current_screen = next_screen

    pygame.quit()


if __name__ == "__main__":
    main()
