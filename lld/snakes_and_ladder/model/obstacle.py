from abc import ABC, abstractmethod

from ..enums.obstacle_type import ObstacleType


class Obstacle(ABC):
    def __init__(self, src: int, dest: int) -> None:
        self._src = src
        self._dest = dest

    @property
    def src(self) -> int:
        return self._src

    @property
    def dest(self) -> int:
        return self._dest

    def move_player(self) -> int:
        return self._dest

    @abstractmethod
    def get_obstacle_type(self) -> ObstacleType:
        pass
