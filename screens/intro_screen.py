import pygame

from screens import routes


INTRO_BOX_HORIZONTAL_MARGIN = 100
INTRO_BOX_HEIGHT = 250
INTRO_BOX_LEFT = 50
INTRO_BOX_TOP_PADDING = 30
INTRO_LINE_SPACING = 70
INTRO_INSTRUCTION_EXTRA_OFFSET = 20
INTRO_CLOCK_FPS = 60
INTRO_BOX_COLOR = (255, 255, 255, 235)
INTRO_TEXT_COLOR = (9, 45, 134)
INTRO_INSTRUCTION_COLOR = (100, 100, 100)


def show_intro_card(screen, font, big_font, width, height, background_image):
    clock = pygame.time.Clock()
    waiting = True

    title = "Has ganado las elecciones"
    subtitle = "Ahora eres el nuevo alcalde de Sevilla."
    instruction = "Pulsa <- o -> para comenzar tu mandato."

    box_width = width - INTRO_BOX_HORIZONTAL_MARGIN
    box_x = INTRO_BOX_LEFT
    box_y = height // 2 - INTRO_BOX_HEIGHT // 2

    while waiting:
        screen.blit(background_image, (0, 0))

        box_surface = pygame.Surface((box_width, INTRO_BOX_HEIGHT), pygame.SRCALPHA)
        pygame.draw.rect(
            box_surface,
            INTRO_BOX_COLOR,
            (0, 0, box_width, INTRO_BOX_HEIGHT),
            border_radius=20,
        )
        screen.blit(box_surface, (box_x, box_y))

        y = box_y + INTRO_BOX_TOP_PADDING
        for text in [title, subtitle]:
            rendered = big_font.render(text, True, INTRO_TEXT_COLOR)
            screen.blit(rendered, (width // 2 - rendered.get_width() // 2, y))
            y += INTRO_LINE_SPACING

        rendered_instruction = font.render(instruction, True, INTRO_INSTRUCTION_COLOR)
        screen.blit(
            rendered_instruction,
            (width // 2 - rendered_instruction.get_width() // 2, y + INTRO_INSTRUCTION_EXTRA_OFFSET),
        )

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return routes.QUIT
            if event.type == pygame.KEYDOWN and event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                waiting = False

        pygame.display.flip()
        clock.tick(INTRO_CLOCK_FPS)

    return None
