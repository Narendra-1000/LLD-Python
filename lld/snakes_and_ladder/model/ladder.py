from ..enums.obstacle_type import ObstacleType
from .obstacle import Obstacle


class Ladder(Obstacle):
    def __init__(self, top: int, bottom: int) -> None:
        super().__init__(bottom, top)

    def get_obstacle_type(self) -> ObstacleType:
        return ObstacleType.LADDER
