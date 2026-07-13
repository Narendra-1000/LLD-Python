from ..enums.obstacle_type import ObstacleType
from ..model.ladder import Ladder
from ..model.obstacle import Obstacle
from ..model.snake import Snake


class ObstacleFactory:
    @staticmethod
    def create_obstacle(type_: ObstacleType, up: int, down: int) -> Obstacle:
        if type_ == ObstacleType.SNAKE:
            return Snake(up, down)
        if type_ == ObstacleType.LADDER:
            return Ladder(up, down)
        raise ValueError("Invalid obstacle type")
