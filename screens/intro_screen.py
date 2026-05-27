from __future__ import annotations

import math
import random
from pathlib import Path

import pygame

import config
from screens import routes


INTRO_CLOCK_FPS = 60
PANEL_MAX_WIDTH = 820
PANEL_MAX_HEIGHT = 430
PANEL_WIDTH_RATIO = 0.64
PANEL_HEIGHT_RATIO = 0.56
PANEL_BORDER_RADIUS = 22
PANEL_FADE_MS = 550
CONFETTI_COUNT = 72
CONFETTI_SAFE_TOP_MARGIN = 12
EMBLEM_PATH = Path(config.ICON_PATH) / "pygame" / "intro" / "no8do_emblem.png"
EMBLEM_MAX_WIDTH = 250
EMBLEM_MAX_HEIGHT = 118

PANEL_FILL = (255, 249, 232)
PANEL_INNER_FILL = (255, 252, 244)
PANEL_SHADOW = (45, 35, 24)
COBALT = config.BLUE_AZULEJO
GOLD = config.ALBERO
GOLD_DARK = (176, 128, 44)
WARM_GRAY = (103, 91, 78)
BLUE_GRAY = (55, 70, 96)
BURGUNDY = config.CLAVEL_RED
CONFETTI_COLORS = (COBALT, GOLD, config.CAL_WHITE, (246, 232, 188), BURGUNDY)


class ConfettiParticle:
    def __init__(self, rng: random.Random, width: int, height: int):
        self.rng = rng
        self.width = width
        self.height = height
        self.reset(initial=True)

    def reset(self, initial: bool = False) -> None:
        self.x = self.rng.uniform(0, self.width)
        self.y = self.rng.uniform(-self.height, self.height * 0.25) if initial else self.rng.uniform(-90, -10)
        self.speed = self.rng.uniform(34, 86)
        self.drift = self.rng.uniform(-22, 22)
        self.phase = self.rng.uniform(0, math.tau)
        self.spin = self.rng.uniform(1.4, 3.8)
        self.size = self.rng.choice((4, 5, 6, 7))
        self.color = self.rng.choice(CONFETTI_COLORS)
        self.alpha = self.rng.randint(120, 190)

    def update(self, dt: float) -> None:
        self.phase += self.spin * dt
        self.x += (self.drift + math.sin(self.phase) * 18) * dt
        self.y += self.speed * dt
        if self.y > self.height + 20:
            self.reset()
        if self.x < -20:
            self.x = self.width + 20
        elif self.x > self.width + 20:
            self.x = -20

    def draw(self, screen: pygame.Surface) -> None:
        piece = pygame.Surface((self.size + 4, self.size + 4), pygame.SRCALPHA)
        color = (*self.color, self.alpha)
        if math.sin(self.phase) > 0:
            pygame.draw.rect(piece, color, (2, 2, self.size, max(2, self.size // 2)), border_radius=1)
        else:
            pygame.draw.ellipse(piece, color, (2, 2, self.size, self.size))
        screen.blit(piece, (int(self.x), int(self.y)))


class ConfettiField:
    def __init__(self, width: int, height: int):
        rng = random.Random(1847)
        self.particles = [ConfettiParticle(rng, width, height) for _ in range(CONFETTI_COUNT)]

    def update(self, dt: float) -> None:
        for particle in self.particles:
            particle.update(dt)

    def draw(self, screen: pygame.Surface) -> None:
        for particle in self.particles:
            if particle.y >= CONFETTI_SAFE_TOP_MARGIN:
                particle.draw(screen)


def show_intro_card(screen, font, big_font, width, height, background_image):
    clock = pygame.time.Clock()
    confetti = ConfettiField(width, height)
    title_font = _load_title_font(width)
    emblem = _load_emblem()
    started_at = pygame.time.get_ticks()

    while True:
        dt = clock.tick(INTRO_CLOCK_FPS) / 1000
        confetti.update(dt)

        screen.blit(background_image, (0, 0))
        confetti.draw(screen)

        elapsed = pygame.time.get_ticks() - started_at
        alpha = min(255, int(255 * elapsed / PANEL_FADE_MS))
        _draw_intro_panel(screen, font, big_font, title_font, emblem, alpha, elapsed)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return routes.QUIT
            if event.type == pygame.KEYDOWN and event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                return None

        pygame.display.flip()


def _load_title_font(width: int) -> pygame.font.Font:
    size = max(34, min(48, int(width * 0.035)))
    font = pygame.font.Font(str(config.CINZEL_BOLD_PATH), size)
    font.set_bold(True)
    return font


def _load_emblem() -> pygame.Surface | None:
    try:
        return pygame.image.load(str(EMBLEM_PATH)).convert_alpha()
    except (FileNotFoundError, pygame.error) as exc:
        print(f"No se pudo cargar el emblema '{EMBLEM_PATH}': {exc}")
        return None


def _draw_intro_panel(
    screen: pygame.Surface,
    font: pygame.font.Font,
    big_font: pygame.font.Font,
    title_font: pygame.font.Font,
    emblem: pygame.Surface | None,
    alpha: int,
    elapsed_ms: int,
) -> None:
    width, height = screen.get_size()
    panel_width = min(PANEL_MAX_WIDTH, int(width * PANEL_WIDTH_RATIO))
    panel_height = min(PANEL_MAX_HEIGHT, int(height * PANEL_HEIGHT_RATIO))
    panel_rect = pygame.Rect(0, 0, panel_width, panel_height)
    panel_rect.center = (width // 2, height // 2 + int(height * 0.035))

    panel_surface = pygame.Surface((panel_width + 34, panel_height + 34), pygame.SRCALPHA)
    local_rect = pygame.Rect(17, 12, panel_width, panel_height)
    _draw_panel_base(panel_surface, local_rect)
    _draw_panel_ornaments(panel_surface, local_rect)
    _draw_panel_content(panel_surface, local_rect, font, big_font, title_font, emblem, elapsed_ms)
    panel_surface.set_alpha(alpha)
    screen.blit(panel_surface, (panel_rect.x - 17, panel_rect.y - 12))


def _draw_panel_base(surface: pygame.Surface, rect: pygame.Rect) -> None:
    shadow_rect = rect.move(0, 10)
    pygame.draw.rect(surface, (*PANEL_SHADOW, 78), shadow_rect, border_radius=PANEL_BORDER_RADIUS)
    pygame.draw.rect(surface, PANEL_FILL, rect, border_radius=PANEL_BORDER_RADIUS)
    pygame.draw.rect(surface, COBALT, rect, 4, border_radius=PANEL_BORDER_RADIUS)
    inner = rect.inflate(-18, -18)
    pygame.draw.rect(surface, PANEL_INNER_FILL, inner, border_radius=PANEL_BORDER_RADIUS - 8)
    pygame.draw.rect(surface, GOLD, inner, 2, border_radius=PANEL_BORDER_RADIUS - 8)
    second = rect.inflate(-34, -34)
    pygame.draw.rect(surface, (*COBALT, 170), second, 1, border_radius=PANEL_BORDER_RADIUS - 12)


def _draw_panel_ornaments(surface: pygame.Surface, rect: pygame.Rect) -> None:
    for x_sign in (-1, 1):
        for y_sign in (-1, 1):
            corner_x = rect.centerx + x_sign * (rect.width // 2 - 42)
            corner_y = rect.centery + y_sign * (rect.height // 2 - 42)
            _draw_corner_flourish(surface, corner_x, corner_y, x_sign, y_sign)

    separator_y = rect.y + int(rect.height * 0.58)
    pygame.draw.line(surface, GOLD_DARK, (rect.x + 130, separator_y), (rect.right - 130, separator_y), 2)
    pygame.draw.circle(surface, GOLD, (rect.centerx, separator_y), 5)
    pygame.draw.circle(surface, COBALT, (rect.centerx, separator_y), 2)
    pygame.draw.line(surface, COBALT, (rect.x + 180, separator_y + 9), (rect.right - 180, separator_y + 9), 1)


def _draw_corner_flourish(surface: pygame.Surface, x: int, y: int, x_sign: int, y_sign: int) -> None:
    arc_rect = pygame.Rect(0, 0, 52, 52)
    arc_rect.center = (x, y)
    start = 0 if x_sign < 0 and y_sign < 0 else 90
    if x_sign > 0 and y_sign < 0:
        start = 90
    elif x_sign > 0 and y_sign > 0:
        start = 180
    elif x_sign < 0 and y_sign > 0:
        start = 270
    pygame.draw.arc(surface, GOLD_DARK, arc_rect, math.radians(start), math.radians(start + 84), 2)
    pygame.draw.circle(surface, COBALT, (x - x_sign * 16, y), 3)
    pygame.draw.circle(surface, GOLD, (x, y - y_sign * 16), 3)


def _draw_panel_content(
    surface: pygame.Surface,
    rect: pygame.Rect,
    font: pygame.font.Font,
    big_font: pygame.font.Font,
    title_font: pygame.font.Font,
    emblem: pygame.Surface | None,
    elapsed_ms: int,
) -> None:
    if emblem:
        scale = min(EMBLEM_MAX_WIDTH / emblem.get_width(), EMBLEM_MAX_HEIGHT / emblem.get_height())
        emblem_size = (int(emblem.get_width() * scale), int(emblem.get_height() * scale))
        emblem_surface = pygame.transform.smoothscale(emblem, emblem_size)
        emblem_rect = emblem_surface.get_rect(center=(rect.centerx, rect.y + 92))
        _draw_emblem_glow(surface, emblem_rect)
        surface.blit(emblem_surface, emblem_rect)

    title = title_font.render("Has ganado las elecciones", True, COBALT)
    subtitle = big_font.render("Ahora eres el nuevo alcalde de Sevilla.", True, BLUE_GRAY)
    instruction = font.render("Pulsa <- o -> para comenzar tu mandato.", True, WARM_GRAY)

    title_rect = title.get_rect(center=(rect.centerx, rect.y + int(rect.height * 0.47)))
    subtitle_rect = subtitle.get_rect(center=(rect.centerx, title_rect.bottom + 42))
    instruction_rect = instruction.get_rect(center=(rect.centerx, rect.bottom - 66))

    surface.blit(title, title_rect)
    surface.blit(subtitle, subtitle_rect)
    _draw_instruction_flourishes(surface, instruction_rect)
    surface.blit(instruction, instruction_rect)


def _draw_emblem_glow(surface: pygame.Surface, rect: pygame.Rect) -> None:
    glow_alpha = 38
    glow = pygame.Surface((rect.width + 34, rect.height + 28), pygame.SRCALPHA)
    pygame.draw.ellipse(glow, (*GOLD, glow_alpha), glow.get_rect())
    surface.blit(glow, (rect.x - 17, rect.y - 14))


def _draw_instruction_flourishes(surface: pygame.Surface, text_rect: pygame.Rect) -> None:
    left_end = text_rect.x - 16
    right_start = text_rect.right + 16
    y = text_rect.centery
    pygame.draw.line(surface, (*GOLD_DARK, 190), (left_end - 62, y), (left_end, y), 1)
    pygame.draw.line(surface, (*GOLD_DARK, 190), (right_start, y), (right_start + 62, y), 1)
    pygame.draw.circle(surface, COBALT, (left_end - 72, y), 3)
    pygame.draw.circle(surface, COBALT, (right_start + 72, y), 3)
