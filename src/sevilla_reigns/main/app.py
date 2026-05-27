import pygame

from sevilla_reigns.config import settings as config
from sevilla_reigns.application.decision_resolver import (
    LEFT_DIRECTION,
    LEFT_OPTION,
    RIGHT_DIRECTION,
    RIGHT_OPTION,
    resolve_decision,
)
from sevilla_reigns.application.effects import get_death_info, get_end_stat
from sevilla_reigns.application.event_manager import EventManager
from sevilla_reigns.application.game_session import GameSession
from sevilla_reigns.application.settings_state import SettingsState
from sevilla_reigns.presentation.screens import routes


NO_EVENTS_MESSAGE = "No quedan más eventos disponibles. Gracias por jugar."
SWIPE_SPEED_DIVISOR = 18
TRANSITION_TILE_SIZE = 150
TRANSITION_FPS = 60
TRANSITION_TILES_PER_STEP = 6


class GameApp:
    def __init__(self):
        from sevilla_reigns.infrastructure.audio.sounds import reproducir_musica
        from sevilla_reigns.infrastructure.transitions.slide_transition import slide_transition
        from sevilla_reigns.presentation.rendering.card_renderer import draw_event, get_choice_index_at_pos
        from sevilla_reigns.presentation.screens.modal_screens import (
            show_exit_confirmation,
            show_final_screen,
            show_reelection_screen,
        )
        from sevilla_reigns.presentation.screens.credits_screen import credits_screen
        from sevilla_reigns.presentation.screens.intro_screen import show_intro_card
        from sevilla_reigns.presentation.screens.settings_screen import settings_screen
        from sevilla_reigns.presentation.screens.start_screen import start_screen
        from sevilla_reigns.presentation.screens.tutorial_screen import tutorial_screen

        self.event_manager = EventManager(config.DATA_PATH / "eventos.json")
        self.session = GameSession(self.event_manager)
        self.settings_state = SettingsState()
        self.background = self._load_background()
        self.current_screen = routes.MENU
        self.running = True

        self.reproducir_musica = reproducir_musica
        self.slide_transition = slide_transition
        self.draw_event = draw_event
        self.get_choice_index_at_pos = get_choice_index_at_pos
        self.show_exit_confirmation = show_exit_confirmation
        self.show_final_screen = show_final_screen
        self.show_reelection_screen = show_reelection_screen
        self.show_intro_card = show_intro_card
        self.screen_handlers = {
            routes.MENU: start_screen,
            routes.TUTORIAL: tutorial_screen,
            routes.SETTINGS: settings_screen,
            routes.CREDITS: credits_screen,
        }

    def run(self):
        self.reproducir_musica()

        while self.running:
            next_screen = self._run_current_screen()

            if next_screen == routes.QUIT:
                self.running = False
                break

            if next_screen is None or next_screen == self.current_screen:
                self.current_screen = next_screen or self.current_screen
                continue

            transition_result = self._transition_to(next_screen)
            if transition_result == routes.QUIT:
                self.running = False
                break
            self.current_screen = next_screen

    def _run_current_screen(self):
        if self.current_screen == routes.GAME:
            return self.run_game_loop()

        handler = self.screen_handlers.get(self.current_screen)
        if handler is None:
            return routes.MENU

        if self.current_screen == routes.MENU:
            return handler(
                config.screen,
                config.WIDTH,
                config.HEIGHT,
                config.FONT_BUTTON,
                config.SUPER_FONT,
                self.background,
            )

        if self.current_screen == routes.SETTINGS:
            return handler(
                config.screen,
                config.WIDTH,
                config.HEIGHT,
                config.FONT_BODY,
                self.background,
                self.settings_state,
            )

        return handler(config.screen, config.WIDTH, config.HEIGHT, config.FONT_BODY, self.background)

    def run_game_loop(self):
        intro_result = self.show_intro_card(
            config.screen,
            config.FONT_SMALL,
            config.FONT_BODY_MEDIUM,
            config.WIDTH,
            config.HEIGHT,
            self.background,
        )
        if intro_result == routes.QUIT:
            return routes.QUIT

        current_event = self.session.start()
        if current_event is None:
            return self.show_final_screen(config.screen, NO_EVENTS_MESSAGE, None)

        swipe_offset = 0
        swipe_direction = 0
        swipe_speed = int(config.WIDTH / SWIPE_SPEED_DIVISOR)

        while True:
            config.clock.tick(config.FPS)
            config.screen.blit(self.background, (0, 0))

            self.draw_event(config.screen, current_event, swipe_offset, self.session.game_state)
            pygame.display.flip()

            route = self._handle_game_input(current_event, swipe_direction)
            if route in (routes.MENU, routes.QUIT):
                return route
            swipe_direction = route

            if swipe_direction == 0:
                continue

            swipe_offset += swipe_speed * swipe_direction
            if abs(swipe_offset) <= config.WIDTH:
                continue

            end_screen = self._check_end_state()
            if end_screen:
                return end_screen

            current_event, show_reelection = self.session.advance_event()
            if show_reelection:
                result = self.show_reelection_screen(config.screen)
                if result == routes.QUIT:
                    return routes.QUIT

            if current_event is None:
                return self.show_final_screen(config.screen, NO_EVENTS_MESSAGE, None)

            swipe_offset = 0
            swipe_direction = 0

    def _handle_game_input(self, event, swipe_direction):
        from sevilla_reigns.infrastructure.audio.sounds import page_sound

        for pygame_event in pygame.event.get():
            if pygame_event.type == pygame.QUIT:
                return routes.QUIT
            if swipe_direction != 0:
                continue

            if pygame_event.type == pygame.MOUSEBUTTONDOWN and pygame_event.button == 1:
                option_index = self.get_choice_index_at_pos(config.screen, pygame_event.pos)
                if option_index is None:
                    continue
                page_sound.play()
                effects = resolve_decision(self.event_manager, self.session.game_state, event, option_index)
                self.session.last_effects = effects
                return LEFT_DIRECTION if option_index == LEFT_OPTION else RIGHT_DIRECTION

            if pygame_event.type != pygame.KEYDOWN:
                continue

            if pygame_event.key == pygame.K_LEFT:
                page_sound.play()
                effects = resolve_decision(
                    self.event_manager,
                    self.session.game_state,
                    event,
                    LEFT_OPTION,
                )
                self.session.last_effects = effects
                return LEFT_DIRECTION
            if pygame_event.key == pygame.K_RIGHT:
                page_sound.play()
                effects = resolve_decision(
                    self.event_manager,
                    self.session.game_state,
                    event,
                    RIGHT_OPTION,
                )
                self.session.last_effects = effects
                return RIGHT_DIRECTION
            if pygame_event.key == pygame.K_ESCAPE:
                confirmation_result = self.show_exit_confirmation(config.screen)
                if confirmation_result == routes.QUIT:
                    return routes.QUIT
                if confirmation_result:
                    return routes.MENU

        return swipe_direction

    def _check_end_state(self):
        cause = get_end_stat(self.session.game_state)
        if not cause:
            return None

        death_text, image = get_death_info(cause, self.session.game_state.stats[cause])
        return self.show_final_screen(config.screen, death_text, image)

    def _transition_to(self, next_screen):
        current_surface = config.screen.copy()
        next_surface = pygame.Surface((config.WIDTH, config.HEIGHT))
        self.draw_screen_preview(next_surface, next_screen)
        next_surface = next_surface.copy()

        return self.slide_transition(
            config.screen,
            config.clock,
            next_screen,
            tile_size=TRANSITION_TILE_SIZE,
            fps=TRANSITION_FPS,
            tiles_per_step=TRANSITION_TILES_PER_STEP,
            draw_screen_func=lambda surface, name: (
                surface.blit(
                    next_surface if name == next_screen else current_surface,
                    (0, 0),
                )
            ),
        )

    def draw_screen_preview(self, surface, screen_name):
        if screen_name in routes.BACKGROUND_SCREENS:
            surface.blit(self.background, (0, 0))
            return

        surface.fill((0, 0, 0))

    def _load_background(self):
        background = pygame.image.load(str(config.IMG_PATH / "fondo_sevillano.png"))
        return pygame.transform.scale(background, (config.WIDTH, config.HEIGHT))
