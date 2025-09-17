import random
import json
import os
from config import eventos
from core.eventmanager import EventManager

# Estado inicial del juego
stats = {
    "religion": 50,
    "people": 50,
    "money": 50,
    "army": 50
}

def get_default_stats():
    return {
        "religion": 50,
        "people": 50,
        "money": 50,
        "army": 50
    }
# Evento actual
event_manager = EventManager("data/eventos.json")
evento_actual = event_manager.seleccionar_evento()

# Función para aplicar los efectos de una opción
def aplicar_efectos(efectos):
    global stats
    for stat, cambio in efectos.items():
        if stat in stats:
            stats[stat] += cambio
            stats[stat] = max(0, min(100, stats[stat]))
        else:
            print(f"Stat desconocida: {stat}")

# Comprobar si se ha llegado a una condición de derrota
def check_fin():
    return any(val <= 0 or val >= 100 for val in stats.values())


