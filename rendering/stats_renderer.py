import pygame

import config
from core.game_state import STAT_LABELS


STAT_AREA_HORIZONTAL_PADDING = 72
STAT_ICON_SIZE = 64
STAT_BAND_HEIGHT = 124
STAT_TOP_Y = 14
STAT_LABEL_Y_OFFSET = 70
STAT_DELTA_Y_OFFSET = 98
STAT_FILL_COLOR = (*config.ALBERO, 210)
STAT_POSITIVE_COLOR = config.OLIVE_GREEN
STAT_NEGATIVE_COLOR = config.CLAVEL_RED
STAT_LABEL_COLOR = config.INK
STAT_MAX_VALUE = 100
BAND_COLOR = (*config.CAL_WHITE, 218)
BAND_BORDER_COLOR = config.BLUE_AZULEJO


def draw_stats(screen, game_state, last_effects=None):
    last_effects = last_effects or {}
    width = screen.get_width()
    band = pygame.Surface((width, STAT_BAND_HEIGHT), pygame.SRCALPHA)
    band.fill(BAND_COLOR)
    screen.blit(band, (0, 0))
    pygame.draw.line(screen, BAND_BORDER_COLOR, (0, STAT_BAND_HEIGHT - 2), (width, STAT_BAND_HEIGHT - 2), 3)

    stat_names = list(game_state.stats.keys())
    num_stats = len(stat_names)
    spacing = (width - STAT_AREA_HORIZONTAL_PADDING * 2) // num_stats

    for i, stat in enumerate(stat_names):
        x = STAT_AREA_HORIZONTAL_PADDING + i * spacing
        icon_x = x + (spacing - STAT_ICON_SIZE) // 2

        base = pygame.transform.scale(config.icons_empty[stat], (STAT_ICON_SIZE, STAT_ICON_SIZE))
        screen.blit(base, (icon_x, STAT_TOP_Y))

        fill_height = int((game_state.stats[stat] / STAT_MAX_VALUE) * STAT_ICON_SIZE)
        fill_surface = pygame.Surface((STAT_ICON_SIZE, fill_height), pygame.SRCALPHA)
        fill_surface.fill(STAT_FILL_COLOR)
        screen.blit(fill_surface, (icon_x, STAT_TOP_Y + STAT_ICON_SIZE - fill_height))

        mask = pygame.transform.scale(config.icons_mask[stat], (STAT_ICON_SIZE, STAT_ICON_SIZE))
        screen.blit(mask, (icon_x, STAT_TOP_Y))

        label = config.FONT.render(STAT_LABELS.get(stat, stat), True, STAT_LABEL_COLOR)
        label_rect = label.get_rect(center=(icon_x + STAT_ICON_SIZE // 2, STAT_TOP_Y + STAT_LABEL_Y_OFFSET))
        screen.blit(label, label_rect)

        if stat in last_effects:
            change = last_effects[stat]
            prefix = "+" if change > 0 else ""
            color = STAT_POSITIVE_COLOR if change > 0 else STAT_NEGATIVE_COLOR
            delta = config.FONT.render(f"{prefix}{change}", True, color)
            delta_rect = delta.get_rect(center=(icon_x + STAT_ICON_SIZE // 2, STAT_TOP_Y + STAT_DELTA_Y_OFFSET))
            screen.blit(delta, delta_rect)
