from ..enums.obstacle_type import ObstacleType
from .obstacle import Obstacle


class Snake(Obstacle):
    def __init__(self, head: int, tail: int) -> None:
        super().__init__(head, tail)

    def get_obstacle_type(self) -> ObstacleType:
        return ObstacleType.SNAKE
