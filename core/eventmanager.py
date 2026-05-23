import json
import random
from core.event import Evento


class EventManager:
    def __init__(self, json_path):
        self.eventos_originales = self.cargar_eventos(json_path)
        self.eventos_activados = set()
        self.eventos_desbloqueados = set()
        self.reset_eventos()

    def reset_eventos(self):
        """Reinicia la lista de eventos disponibles barajandolos."""
        self.eventos_disponibles = self.eventos_originales[:]
        random.shuffle(self.eventos_disponibles)

    def cargar_eventos(self, path):
        with open(path, "r", encoding="utf-8") as f:
            eventos_raw = json.load(f)
        return [Evento(**e) for e in eventos_raw]

    def get_eventos_posibles(self):
        posibles = []
        for evento in self.eventos_disponibles:
            if evento.id in self.eventos_activados:
                continue

            if evento.requisitos and not all(req in self.eventos_desbloqueados for req in evento.requisitos):
                continue

            posibles.append(evento)
        return posibles

    def seleccionar_evento(self):
        posibles = self.get_eventos_posibles()

        if not posibles:
            self.eventos_activados.clear()
            self.reset_eventos()
            posibles = self.get_eventos_posibles()

        if not posibles:
            return None

        elegido = random.choice(posibles)
        self.eventos_disponibles.remove(elegido)
        return elegido

    def aplicar_decision(self, evento, lado):
        opcion = evento.options[lado]
        self.eventos_activados.add(evento.id)

        if opcion.desbloquea:
            desbloqueos = opcion.desbloquea
            if isinstance(desbloqueos, list):
                self.eventos_desbloqueados.update(desbloqueos)
            elif isinstance(desbloqueos, str):
                self.eventos_desbloqueados.add(desbloqueos)

        return opcion.effects
