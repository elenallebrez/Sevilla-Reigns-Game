import pygame
from core.sounds import click_sound

class Button:
    def __init__(self, text, x, y, width, height, callback, font, color=(200,200,200), hover_color=(255,255,255)):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.callback = callback
        self.font = font
        self.color = color
        self.hover_color = hover_color

    def draw(self, screen):
        mouse = pygame.mouse.get_pos()
        is_hovered = self.rect.collidepoint(mouse)
        pygame.draw.rect(screen, self.hover_color if is_hovered else self.color, self.rect)
        pygame.draw.rect(screen, (0, 0, 0), self.rect, 2)

        text_surf = self.font.render(self.text, True, (0, 0, 0))
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            click_sound.play()
            self.callback()
