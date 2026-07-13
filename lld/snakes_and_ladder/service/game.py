import random
from collections import deque

from ..enums.obstacle_type import ObstacleType
from ..factory.obstacle_factory import ObstacleFactory
from ..model.board import Board
from ..model.dice import Dice
from ..model.obstacle import Obstacle
from ..model.player import Player


class Game:
    def __init__(
        self, size: int, no_of_ladders: int, no_of_snakes: int, no_of_dice: int
    ) -> None:
        self._no_of_snakes = no_of_snakes
        self._no_of_ladders = no_of_ladders
        self._board = Board(size)
        self._players: deque[Player] = deque()
        self._dice = Dice(no_of_dice)

        self._init_board_obstacles()

    @property
    def no_of_snakes(self) -> int:
        return self._no_of_snakes

    @property
    def no_of_ladders(self) -> int:
        return self._no_of_ladders

    @property
    def board(self) -> Board:
        return self._board

    @property
    def players(self) -> deque[Player]:
        return self._players

    @property
    def dice(self) -> Dice:
        return self._dice

    def _init_board_obstacles(self) -> None:
        self._generate_obstacles(self._no_of_snakes, ObstacleType.SNAKE)
        self._generate_obstacles(self._no_of_ladders, ObstacleType.LADDER)

    def _generate_obstacles(self, count: int, type_: ObstacleType) -> None:
        rng = random.Random()
        size = self._board.size

        while count > 0:
            up = rng.randint(2, size)
            down = rng.randint(1, up - 1)

            obstacle: Obstacle = ObstacleFactory.create_obstacle(type_, up, down)
            if self._board.add_obstacle(obstacle):
                count -= 1

    def add_player(self, player: Player) -> None:
        self._players.append(player)

    def start_game(self) -> None:
        self._board.print_board(self._players)

        while len(self._players) > 1:
            curr_player = self._players.popleft()
            print("-----------------------------------")

            dice_roll = self._dice.roll()
            print(f"{curr_player.name} rolled {dice_roll}")

            new_position = self._board.get_new_position(curr_player, dice_roll)

            if new_position == curr_player.position:
                self._players.append(curr_player)
                continue

            curr_player.position = new_position

            if new_position == self._board.size:
                print(f"{curr_player.name} has won the game!")
            else:
                self._players.append(curr_player)

            self._board.print_board(self._players)
