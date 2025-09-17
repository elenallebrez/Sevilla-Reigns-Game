from core.game_state import stats
import json
import os
import random

with open((r'C:\Users\elena\Documents\Portfolio\Sevilla\data\motivos_muerte.json'), encoding='utf-8') as f:
    MOTIVOS_MUERTE = json.load(f)

def aplicar_efectos(efectos):
    for stat, cambio in efectos.items():
        if stat in stats:
            stats[stat] += cambio
            stats[stat] = max(0, min(100, stats[stat]))
        else:
            print(f"Stat desconocida: {stat}")

def check_fin():
    for stat, val in stats.items():
        if val <= 0 or val >= 100:
            return stat
    return None

def get_info_muerte(stat, value):
    if stat not in MOTIVOS_MUERTE:
        return "Has abdicado... pero no sabemos por que", None

    clave = "zero" if value <= 0 else "hundred"
    opciones = MOTIVOS_MUERTE[stat].get(clave, [])

    if not opciones:
        return "Has muerto de forma misteriosa...", None

    eleccion = random.choice(opciones)
    return eleccion["motivo"], os.path.join("resources", "images", eleccion["imagen"])
