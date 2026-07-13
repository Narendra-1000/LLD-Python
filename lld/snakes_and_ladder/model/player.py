from dataclasses import dataclass, field


@dataclass
class Player:
    name: str
    position: int = field(default=1)
