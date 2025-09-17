class Opcion:
    def __init__(self, text, effects, desbloquea=None):
        self.text = text
        self.effects = effects
        self.desbloquea = desbloquea

class Evento:
    def __init__(self, id, title, description, options, image=None, requisitos=None):
        self.id = id
        self.title = title
        self.description = description
        self.options = [Opcion(**opt) for opt in options]
        self.image = image
        self.requisitos = requisitos or []
