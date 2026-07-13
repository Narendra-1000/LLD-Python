from dataclasses import dataclass, field
from typing import Optional

from .obstacle import Obstacle


@dataclass
class Cell:
    position: int
    obstacle: Optional[Obstacle] = field(default=None)

    def has_obstacle(self) -> bool:
        return self.obstacle is not None

    def get_final_position(self) -> int:
        return self.obstacle.move_player() if self.has_obstacle() else self.position
