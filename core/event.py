from dataclasses import dataclass, field


@dataclass
class Option:
    text: str
    effects: dict[str, int]
    desbloquea: str | list[str] | None = None

    @property
    def unlocks(self) -> str | list[str] | None:
        return self.desbloquea


@dataclass
class Event:
    id: str
    title: str
    description: str
    options: list[Option]
    image: str | None = None
    requisitos: list[str] = field(default_factory=list)

    def __init__(
        self,
        id: str,
        title: str,
        description: str,
        options: list[dict],
        image: str | None = None,
        requisitos: list[str] | None = None,
    ) -> None:
        self.id = id
        self.title = title
        self.description = description
        self.options = [Option(**option) for option in options]
        self.image = image
        self.requisitos = requisitos or []

    @property
    def requirements(self) -> list[str]:
        return self.requisitos
