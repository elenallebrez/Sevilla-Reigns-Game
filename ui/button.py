from pathlib import Path

import pygame

import config
from core.sounds import click_sound


HOVER_EASING = 0.16
HOVER_LIFT = 0
HOVER_SCALE = 0
ICON_GAP = 10
ICON_SIZE_RATIO = 0.58
ICON_FRAME_DURATION_MS = 105
ICON_ANIMATION_DIRS = {
    "tower": "comenzar",
    "book": "tutorial",
    "gear": "ajustes",
    "flower": "creditos",
    "door": "salir",
}
_surface_cache = {}

BUTTON_STYLES = {
    "secondary": {
        "fill": (226, 220, 207),
        "hover": config.CAL_WHITE,
        "focus": config.ALBERO_LIGHT,
        "border": config.BLUE_AZULEJO,
        "text": config.INK,
        "icon": config.BLUE_AZULEJO,
        "accent": config.ALBERO,
    },
    "primary": {
        "fill": config.ALBERO,
        "hover": config.ALBERO_LIGHT,
        "focus": config.ALBERO_LIGHT,
        "border": config.BLUE_AZULEJO,
        "text": config.INK,
        "icon": config.BLUE_AZULEJO,
        "accent": config.CAL_WHITE,
    },
    "danger": {
        "fill": config.CLAVEL_RED,
        "hover": (188, 50, 54),
        "focus": (210, 74, 77),
        "border": (92, 22, 24),
        "text": config.CAL_WHITE,
        "icon": config.CAL_WHITE,
        "accent": config.ALBERO,
    },
}


class Button:
    def __init__(
        self,
        text,
        x,
        y,
        width,
        height,
        callback,
        font,
        color=None,
        hover_color=None,
        focus_color=None,
        disabled=False,
        variant="secondary",
        icon=None,
    ):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.callback = callback
        self.font = font
        self.style = BUTTON_STYLES.get(variant, BUTTON_STYLES["secondary"]).copy()
        self.color = color or self.style["fill"]
        self.hover_color = hover_color or self.style["hover"]
        self.focus_color = focus_color or self.style["focus"]
        self.disabled = disabled
        self.focused = False
        self.icon = icon
        self.animated_icon = AnimatedIcon(icon) if icon else None
        self.hover_progress = 0.0

    def set_focused(self, focused):
        self.focused = focused

    def draw(self, screen):
        mouse = pygame.mouse.get_pos()
        is_hovered = self.rect.collidepoint(mouse)
        target_progress = 1.0 if is_hovered else 0.0
        self.hover_progress += (target_progress - self.hover_progress) * HOVER_EASING

        color = self.color
        if self.focused:
            color = self.focus_color
        if is_hovered:
            color = self.hover_color

        visual_rect = self._get_visual_rect()
        self._draw_shadow(screen, visual_rect)

        pygame.draw.rect(screen, color, visual_rect, border_radius=9)
        border_width = 4 if self.focused else 2
        pygame.draw.rect(screen, self.style["border"], visual_rect, border_width, border_radius=9)
        self._draw_gold_detail(screen, visual_rect)

        self._draw_content(screen, visual_rect, is_hovered)

    def _get_visual_rect(self):
        scale_padding_x = int(self.rect.width * HOVER_SCALE * self.hover_progress)
        scale_padding_y = int(self.rect.height * HOVER_SCALE * self.hover_progress)
        lift = int(HOVER_LIFT * self.hover_progress)
        return self.rect.inflate(scale_padding_x, scale_padding_y).move(0, -lift)

    def _draw_shadow(self, screen, rect):
        shadow_alpha = int(95 + 55 * self.hover_progress)
        shadow_padding = int(3 + 3 * self.hover_progress)
        shadow_offset_y = int(6 + 5 * self.hover_progress)
        shadow_rect = pygame.Rect(
            shadow_padding,
            shadow_padding,
            rect.width + shadow_padding * 2,
            rect.height + shadow_padding * 2,
        )
        shadow_surface = pygame.Surface(shadow_rect.size, pygame.SRCALPHA)
        pygame.draw.rect(
            shadow_surface,
            (*config.TILE_SHADOW, shadow_alpha),
            shadow_surface.get_rect(),
            border_radius=11,
        )
        screen.blit(shadow_surface, (rect.x + 4 - shadow_padding, rect.y + shadow_offset_y - shadow_padding))

    def _draw_gold_detail(self, screen, rect):
        inset = 5
        detail_rect = rect.inflate(-inset * 2, -inset * 2)
        pygame.draw.rect(screen, self.style["accent"], detail_rect, 1, border_radius=6)

    def _draw_content(self, screen, rect, is_hovered):
        text_surf = self.font.render(self.text, True, self.style["text"])
        if not self.icon:
            text_rect = text_surf.get_rect(center=rect.center)
            screen.blit(text_surf, text_rect)
            return

        icon_size = int(self.rect.height * ICON_SIZE_RATIO)
        total_width = icon_size + ICON_GAP + text_surf.get_width()
        start_x = rect.centerx - total_width // 2
        icon_rect = pygame.Rect(start_x, rect.centery - icon_size // 2, icon_size, icon_size)
        text_rect = text_surf.get_rect(midleft=(icon_rect.right + ICON_GAP, rect.centery))

        if self.animated_icon:
            self.animated_icon.draw(screen, icon_rect, is_hovered)
        screen.blit(text_surf, text_rect)

    def activate(self):
        if self.disabled:
            return

        click_sound.play()
        self.callback()

    def handle_event(self, event):
        if self.disabled:
            return

        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            self.activate()
        elif event.type == pygame.KEYDOWN and self.focused and event.key in (pygame.K_RETURN, pygame.K_SPACE):
            self.activate()


class AnimatedIcon:
    def __init__(self, icon):
        self.icon = icon
        self.frames = load_icon_frames(icon)
        self.frames_by_size = {}
        self.hover_started_at = None

    def draw(self, screen, rect, is_hovered):
        if not self.frames:
            return

        frame_index = self._frame_index(is_hovered)
        frame = self._get_sized_frames(rect.size)[frame_index]
        screen.blit(frame, frame.get_rect(center=rect.center))

    def _frame_index(self, is_hovered):
        if not is_hovered:
            self.hover_started_at = None
            return 0

        now = pygame.time.get_ticks()
        if self.hover_started_at is None:
            self.hover_started_at = now

        elapsed = now - self.hover_started_at
        return (elapsed // ICON_FRAME_DURATION_MS) % len(self.frames)

    def _get_sized_frames(self, size):
        if size not in self.frames_by_size:
            self.frames_by_size[size] = [
                pygame.transform.smoothscale(frame, size) if frame.get_size() != size else frame
                for frame in self.frames
            ]
        return self.frames_by_size[size]


def load_icon_frames(icon):
    if icon in _surface_cache:
        return _surface_cache[icon]

    animation_dir = ICON_ANIMATION_DIRS.get(icon)
    if animation_dir:
        frames = load_animation_frames(animation_dir)
        if frames:
            _surface_cache[icon] = frames
            return frames

    static_surface = load_static_icon(icon)
    frames = [static_surface] if static_surface else []
    _surface_cache[icon] = frames
    return frames


def load_animation_frames(animation_dir):
    frames_path = Path(config.ICON_PATH) / "animated" / animation_dir
    frame_files = sorted(frames_path.glob("*.png"))
    frames = []
    for frame_file in frame_files:
        try:
            frames.append(pygame.image.load(str(frame_file)).convert_alpha())
        except pygame.error as exc:
            print(f"No se pudo cargar el frame '{frame_file}': {exc}")
    return frames


def load_static_icon(icon):
    static_filename = ICON_ANIMATION_DIRS.get(icon)
    if not static_filename:
        return None

    static_path = Path(config.ICON_PATH) / "static" / f"{static_filename}.png"
    return load_surface(static_path)


def load_surface(path):
    try:
        return pygame.image.load(str(path)).convert_alpha()
    except (FileNotFoundError, pygame.error) as exc:
        print(f"No se pudo cargar el icono '{path}': {exc}")
        return None
