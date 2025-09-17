import pygame
import json
import os
import random
from core.event import Evento
from config import WIDTH, HEIGHT, FPS, screen, clock, FONT, WHITE, SUPER_FONT
from core.effects import aplicar_efectos, check_fin, get_info_muerte
from core.renderer import draw_stats, draw_event, mostrar_pantalla_final, mostrar_confirmacion_salida, mostrar_pantalla_reeleccion
from screens.start_screen import start_screen
from screens.tutorial_screen import tutorial_screen
from core.game_state import stats, get_default_stats
from core.sounds import reproducir_musica, page_sound
from screens.settings_screen import settings_screen
from screens.intro import mostrar_carta_introductoria
from core.eventmanager import EventManager
from core.transition import slide_transition
from screens.credits_screen import credits_screen

# Cargar eventos desde JSON
event_manager = EventManager("data/eventos.json")
evento_actual = event_manager.seleccionar_evento()

background_path = os.path.join("resources", "images", "fondo.png")
background = pygame.image.load(background_path)
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

def bucle_del_juego(screen):
    global stats
    stats.clear()
    stats.update(get_default_stats())
    mostrar_carta_introductoria(screen, FONT, FONT, WIDTH, HEIGHT, background)
    swipe_speed = int(WIDTH / 18)
    evento_actual = event_manager.seleccionar_evento()

    if evento_actual is None:
        texto_final = "No quedan más eventos disponibles. ¡Gracias por jugar!"
        next_screen = mostrar_pantalla_final(screen, texto_final)
        return next_screen

    swipe_offset = 0
    swipe_direction = 0
    cartas_jugadas = 0

    running = True
    while running:

        clock.tick(FPS)
        screen.fill((200, 200, 255))
        
        draw_stats(screen)
        draw_event(screen, evento_actual, swipe_offset)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            elif event.type == pygame.KEYDOWN and swipe_direction == 0:
                if event.key == pygame.K_LEFT:
                    page_sound.play()
                    lado_elegido = 0
                    swipe_direction = -1
                elif event.key == pygame.K_RIGHT:
                    page_sound.play()
                    lado_elegido = 1
                    swipe_direction = 1
                elif event.key == pygame.K_ESCAPE:
                    salir = mostrar_confirmacion_salida(screen)
                    if salir:
                        return "menu"

            if swipe_direction != 0:
                    cambios = event_manager.aplicar_decision(evento_actual, lado_elegido)
                    aplicar_efectos(cambios)

        if swipe_direction != 0:
            swipe_offset += swipe_speed * swipe_direction
            if abs(swipe_offset) > WIDTH:
                causa = check_fin()
                if causa:
                    texto_muerte, imagen = get_info_muerte(causa, stats[causa])
                    next_screen = mostrar_pantalla_final(screen, texto_muerte, imagen)
                    return next_screen 
                else:
                    cartas_jugadas += 1  # 🔹 sumamos carta jugada
                    if cartas_jugadas >= 30:  # 🔹 condición reelección
                        mostrar_pantalla_reeleccion(
                            screen
                        )
                        stats.clear()
                        stats.update(get_default_stats())
                        cartas_jugadas = 0 

                    evento_actual = event_manager.seleccionar_evento()
                    swipe_offset = 0
                    swipe_direction = 0


def draw_real_screen(surface, screen_name):
    """
    Dibuja la pantalla correspondiente en 'surface' sin ejecutar la lógica interactiva.
    Útil para transiciones.
    """
    WIDTH, HEIGHT = surface.get_size()

    if screen_name == "menu":
        surface.blit(background, (0, 0))

    elif screen_name == "tutorial":
        surface.blit(background, (0, 0)) 

    elif screen_name == "game":
        surface.fill((0, 0, 0))

    elif screen_name == "settings":
        surface.blit(background, (0, 0)) 

    elif screen_name == "credits":
        surface.blit(background, (0, 0)) 

    else:
        surface.fill((0, 0, 0))


current_screen = "menu"
running = True
reproducir_musica()

while running:
    pantalla_actual_surface = pygame.Surface((WIDTH, HEIGHT))

    if current_screen == "menu":
        next_screen = start_screen(screen, WIDTH, HEIGHT, FONT, SUPER_FONT, background)
    elif current_screen == "tutorial":
        next_screen = tutorial_screen(screen, WIDTH, HEIGHT, FONT, background)
    elif current_screen == "game":
        next_screen = bucle_del_juego(screen)
    elif current_screen == "settings":
        next_screen = settings_screen(screen, WIDTH, HEIGHT, FONT, background)
    elif current_screen == "credits":
        next_screen = credits_screen(screen, WIDTH, HEIGHT, FONT, background)
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

    # --- Captura de la pantalla actual ---
    pantalla_actual = screen.copy()

    # --- Dibujamos la próxima pantalla en un surface temporal ---
    pantalla_siguiente_surface = pygame.Surface((WIDTH, HEIGHT))
    draw_real_screen(pantalla_siguiente_surface, next_screen)
    pantalla_siguiente = pantalla_siguiente_surface.copy()

    # --- Transición usando las capturas ---
    slide_transition(
        screen, clock, next_screen,
        tile_size=150, fps=60, tiles_per_step=6,
        draw_screen_func=lambda surf, name: (
            surf.blit(pantalla_siguiente if name == next_screen else pantalla_actual, (0, 0))
        )
    )

    current_screen = next_screen

pygame.quit()
