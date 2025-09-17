import json
import random
from core.event import Evento

class EventManager:
    def __init__(self, json_path):
        # Guardamos todos los eventos originales
        self.eventos_originales = self.cargar_eventos(json_path)
        self.reset_eventos()
        self.eventos_activados = set()
        self.eventos_desbloqueados = set()

    def reset_eventos(self):
        """Reinicia la lista de eventos disponibles barajándolos."""
        self.eventos_disponibles = self.eventos_originales[:]
        random.shuffle(self.eventos_disponibles)

    def cargar_eventos(self, path):
        with open(path, "r", encoding="utf-8") as f:
            eventos_raw = json.load(f)
        return [Evento(**e) for e in eventos_raw]

    def seleccionar_evento(self):
        posibles = []
        for evento in self.eventos_disponibles:
            if evento.title in self.eventos_activados:
                continue

            # Si el evento tiene requisitos, solo puede aparecer si están en desbloqueados
            if hasattr(evento, "requisitos") and evento.requisitos:
                if not all(req in self.eventos_desbloqueados for req in evento.requisitos):
                    continue

            posibles.append(evento)

        if not posibles:
            # Si no hay posibles, reseteamos y seguimos
            self.reset_eventos()
            return self.seleccionar_evento()

        elegido = random.choice(posibles)
        self.eventos_disponibles.remove(elegido)  # Lo quitamos para evitar repetirlo de inmediato
        return elegido

    def aplicar_decision(self, evento, lado):
        cambios = evento.options[lado].effects
        self.eventos_activados.add(evento.title)

        # Desbloqueos
        if hasattr(evento.options[lado], "desbloquea") and evento.options[lado].desbloquea:
            desbloqueos = evento.options[lado].desbloquea
            if isinstance(desbloqueos, list):
                for e in desbloqueos:
                    self.eventos_desbloqueados.add(e)
            elif isinstance(desbloqueos, str):
                self.eventos_desbloqueados.add(desbloqueos)

        return cambios
