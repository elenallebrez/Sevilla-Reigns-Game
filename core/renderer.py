import pygame
import os
import sys
from core.game_state import stats
from core.sounds import click_sound, reproducir_muerte, reproducir_musica
from config import icons_empty, icons_mask, BIG_FONT, FONT, WHITE, BLACK, WIDTH, HEIGHT, MEDIUM_FONT, clock, FPS

def draw_stats(screen):
    width = screen.get_width()
    stat_names = list(stats.keys())
    num_stats = len(stat_names)
    spacing = (width - 40) // num_stats
    icon_size = 80  # tamaño final
    top_y = 20

    for i, stat in enumerate(stat_names):
        x = 20 + i * spacing
        icon_x = x + (spacing - icon_size) // 2

        # Base: silueta vacía
        base = pygame.transform.scale(icons_empty[stat], (icon_size, icon_size))
        screen.blit(base, (icon_x, top_y))

        # Relleno
        fill_height = int((stats[stat] / 100) * icon_size)
        fill_surface = pygame.Surface((icon_size, fill_height), pygame.SRCALPHA)
        fill_surface.fill((255, 215, 0, 200))  # dorado semitransparente
        screen.blit(fill_surface, (icon_x, top_y + icon_size - fill_height))

        # Silueta rellena (para recortar el relleno con la forma exacta)
        mask = pygame.transform.scale(icons_mask[stat], (icon_size, icon_size))
        screen.blit(mask, (icon_x, top_y))

def draw_text_wrapped(surface, text, font, color, rect, line_spacing=5):
    words = text.split(' ')
    lines = []
    current_line = ''

    for word in words:
        test_line = current_line + word + ' '
        if font.size(test_line)[0] <= rect.width:
            current_line = test_line
        else:
            lines.append(current_line.strip())
            current_line = word + ' '
    lines.append(current_line.strip())

    y = rect.y
    for line in lines:
        rendered_text = font.render(line, True, color)
        surface.blit(rendered_text, (rect.x + (rect.width - rendered_text.get_width()) // 2, y))
        y += rendered_text.get_height() + line_spacing

def draw_event(screen, evento, swipe_offset): 
    width = screen.get_width()
    height = screen.get_height()

    stats_height = 120  # área ocupada por draw_stats
    top_offset = stats_height  # margen debajo de stats
    bottom_padding = 30  # margen inferior

    card_width = width - 200
    card_height = height - top_offset - bottom_padding
    card_x = (width - card_width) // 2
    card_y = top_offset

    # Dibujo de la carta
    card_rect = pygame.Rect(card_x + swipe_offset, card_y, card_width, card_height)
    pygame.draw.rect(screen, WHITE, card_rect)
    pygame.draw.rect(screen, BLACK, card_rect, 3)

    # Título centrado
    title = BIG_FONT.render(evento.title, True, BLACK)
    title_y = card_y + 20
    screen.blit(title, (card_rect.centerx - title.get_width() // 2, title_y))

    # Imagen del evento (máximo 70% del ancho de la carta)
    image_width = int(card_width * 0.7)
    image_height = int(card_height* 0.6)
    image_x = card_rect.centerx - image_width // 2
    image_y = title_y + title.get_height() + 20

    if evento.image:
        try:
            ruta_imagen = os.path.join("resources", "images", evento.image)
            imagen_evento = pygame.image.load(ruta_imagen).convert_alpha()

            # Tamaño original
            orig_w, orig_h = imagen_evento.get_size()
            image_y = title_y + title.get_height() + 20

            # Definir tamaño máximo permitido dentro de la carta
            espacio_libre = card_rect.bottom - 140 - image_y
            max_w = int(card_width * 0.8)
            max_h = espacio_libre  # por ejemplo, 40% del alto de la carta

            # Escalar manteniendo proporción
            scale = min(max_w / orig_w, max_h / orig_h)
            new_w = int(orig_w * scale)
            new_h = int(orig_h * scale)

            imagen_evento = pygame.transform.smoothscale(imagen_evento, (new_w, new_h))

            # Centrar en la carta
            image_x = card_rect.centerx - new_w // 2

            screen.blit(imagen_evento, (image_x, image_y))

        except Exception as e:
            print(f"No se pudo cargar la imagen: {evento.image}, error: {e}")


    # Descripción (debajo de la imagen)
    desc_y = image_y + image_height + 20
    desc_height = 100
    desc_rect = pygame.Rect(card_rect.left + 40, desc_y, card_width - 80, desc_height)

    draw_text_wrapped(screen, evento.description, FONT, BLACK, desc_rect)

    # Opciones (abajo de todo)
    izquierda = FONT.render(evento.options[0].text, True, BLACK)
    derecha = FONT.render(evento.options[1].text, True, BLACK)

    opciones_y = card_rect.bottom - 60

    screen.blit(izquierda, (card_rect.left + 40 + swipe_offset, opciones_y))
    screen.blit(derecha, (card_rect.right - derecha.get_width() - 40 + swipe_offset, opciones_y))

def mostrar_pantalla_final(screen, texto_muerte, imagen_fondo):
    width, height = screen.get_size()

    pygame.mixer.music.stop()
    reproducir_muerte()

    if imagen_fondo and os.path.exists(imagen_fondo):
        fondo = pygame.image.load(imagen_fondo).convert()
        fondo = pygame.transform.scale(fondo, (width, height))
        screen.blit(fondo, (0, 0))
    else:
        screen.fill((30, 0, 0))  # fallback por si no hay imagen

    # Opcional: oscurecer el fondo
    overlay = pygame.Surface((width, height))
    overlay.set_alpha(150)
    overlay.fill((0, 0, 0))
    screen.blit(overlay, (0, 0))

    # Caja central con texto
    box_width = width - 150
    box_height = 200
    box_x = (width - box_width) // 2
    box_y = (height - box_height) // 2
    box_rect = pygame.Rect(box_x, box_y, box_width, box_height)

    pygame.draw.rect(screen, (80, 0, 0), box_rect, border_radius=20)
    pygame.draw.rect(screen, (200, 0, 0), box_rect, 4, border_radius=20)

    titulo = BIG_FONT.render("Mocion de censura", True, (255, 255, 255))
    causa = FONT.render(texto_muerte, True, (255, 255, 255))
    instruccion = FONT.render("Pulsa cualquier boton para volver al menu", True, (200, 200, 200))

    screen.blit(titulo, (width // 2 - titulo.get_width() // 2, box_y + 30))
    screen.blit(causa, (width // 2 - causa.get_width() // 2, box_y + 100))
    screen.blit(instruccion, (width // 2 - instruccion.get_width() // 2, box_y + box_height + 40))

    pygame.display.flip()
    esperando = True
    while esperando:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                esperando = False

    # Fade out
    fade_surface = pygame.Surface((width, height))
    fade_surface.fill((0, 0, 0))
    for alpha in range(0, 255, 5):
        fade_surface.set_alpha(alpha)
        screen.blit(fade_surface, (0, 0))
        pygame.display.flip()
        pygame.time.delay(30)

    pygame.mixer.music.fadeout(800)
    reproducir_musica()
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1, fade_ms=800)

    return "menu"

def mostrar_confirmacion_salida(screen):
    clock = pygame.time.Clock()

    # Dimensiones
    box_width = 500
    box_height = 200
    final_y = (HEIGHT - box_height) // 2
    box_x = (WIDTH - box_width) // 2
    start_y = HEIGHT  # Empieza desde abajo

    # Fuentes
    font_title = MEDIUM_FONT
    font_option = FONT

    # Animación: subida desde abajo
    current_y = start_y
    animation_speed = 20  # píxeles por frame

    salir = None  # Resultado final

    while True:
        screen_copy = screen.copy()  # Captura la pantalla actual

        # Capa oscura encima (simula desenfoque ligero)
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(150)
        overlay.fill((0, 0, 0))
        screen.blit(screen_copy, (0, 0))
        screen.blit(overlay, (0, 0))

        # Actualiza posición de la caja (animación hacia arriba)
        if current_y > final_y:
            current_y -= animation_speed
            if current_y < final_y:
                current_y = final_y

        # Caja de confirmación
        box_rect = pygame.Rect(box_x, current_y, box_width, box_height)
        pygame.draw.rect(screen, (255, 255, 255), box_rect, border_radius=15)
        pygame.draw.rect(screen, (0, 0, 0), box_rect, 3, border_radius=15)

        # Texto
        texto = font_title.render("¿Seguro que quieres salir?", True, BLACK)
        screen.blit(texto, (box_x + (box_width - texto.get_width()) // 2, current_y + 30))

        # Botones
        button_width = 120
        button_height = 40
        spacing = 40

        yes_rect = pygame.Rect(
            box_x + (box_width // 2 - button_width - spacing // 2),
            current_y + 110,
            button_width,
            button_height
        )
        no_rect = pygame.Rect(
            box_x + (box_width // 2 + spacing // 2),
            current_y + 110,
            button_width,
            button_height
        )

        pygame.draw.rect(screen, (200, 0, 0), yes_rect, border_radius=10)
        pygame.draw.rect(screen, (0, 150, 0), no_rect, border_radius=10)

        yes_text = font_option.render("Si", True, WHITE)
        no_text = font_option.render("No", True, WHITE)
        screen.blit(yes_text, (yes_rect.centerx - yes_text.get_width() // 2, yes_rect.centery - yes_text.get_height() // 2))
        screen.blit(no_text, (no_rect.centerx - no_text.get_width() // 2, no_rect.centery - no_text.get_height() // 2))

        pygame.display.flip()

        # Solo permite elegir cuando la animación termina
        if current_y == final_y:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return True
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if yes_rect.collidepoint(event.pos):
                        click_sound.play()
                        return True
                    elif no_rect.collidepoint(event.pos):
                        click_sound.play()
                        return False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_y:
                        return True
                    elif event.key == pygame.K_n or event.key == pygame.K_ESCAPE:
                        return False

        clock.tick(60)

def mostrar_pantalla_reeleccion(screen, mensaje="Has sido reelegido"):
    screen.fill((230, 230, 255))

    # Renderizar texto centrado
    lineas = mensaje.split("\n")
    y_inicial = HEIGHT // 3

    for i, linea in enumerate(lineas):
        texto = FONT.render(linea, True, (0, 0, 0))
        rect = texto.get_rect(center=(WIDTH // 2, y_inicial + i * 50))
        screen.blit(texto, rect)

    # Texto pequeño abajo
    texto_continuar = pygame.font.Font(None, 30).render(
        "Presiona cualquier tecla para continuar...", True, (100, 100, 100)
    )
    rect_continuar = texto_continuar.get_rect(center=(WIDTH // 2, HEIGHT - 60))
    screen.blit(texto_continuar, rect_continuar)

    pygame.display.flip()

    # Esperar input
    esperando = True
    while esperando:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                esperando = False

    return None
