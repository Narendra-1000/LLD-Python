import math
from collections import deque
from typing import Deque

from ..enums.obstacle_type import ObstacleType
from .cell import Cell
from .obstacle import Obstacle
from .player import Player


class Board:
    def __init__(self, size: int) -> None:
        self._size = size
        self._side_length = int(math.sqrt(size))
        self._grid: list[list[Cell]] = [
            [None] * self._side_length for _ in range(self._side_length)  # type: ignore[list-item]
        ]

        position = 1
        left_to_right = True

        for i in range(self._side_length - 1, -1, -1):
            if left_to_right:
                for j in range(self._side_length):
                    self._grid[i][j] = Cell(position)
                    position += 1
            else:
                for j in range(self._side_length - 1, -1, -1):
                    self._grid[i][j] = Cell(position)
                    position += 1
            left_to_right = not left_to_right

    @property
    def size(self) -> int:
        return self._size

    def _get_row(self, position: int) -> int:
        row = (position - 1) // self._side_length
        return self._side_length - 1 - row

    def _get_col(self, position: int) -> int:
        row = self._get_row(position)
        col = (position - 1) % self._side_length
        return self._side_length - 1 - col if row % 2 == 0 else col

    def _get_cell(self, position: int) -> Cell:
        return self._grid[self._get_row(position)][self._get_col(position)]

    def add_obstacle(self, obstacle: Obstacle) -> bool:
        src_cell = self._get_cell(obstacle.src)
        dest_cell = self._get_cell(obstacle.dest)

        if src_cell.has_obstacle() or dest_cell.has_obstacle():
            return False

        src_cell.obstacle = obstacle
        return True

    def get_new_position(self, player: Player, offset: int) -> int:
        new_position = player.position + offset

        if new_position > self._size:
            print("You are going out of the board! Better luck next time!")
            return player.position

        cell = self._grid[self._get_row(new_position)][self._get_col(new_position)]
        final_position = cell.get_final_position()

        if final_position < new_position:
            print(f"Oops! Snake has bitten {player.name}")
        elif final_position > new_position:
            print(f"Congratulations! {player.name} moved up through a ladder")
        else:
            print(f"{player.name} moved from {player.position} to {new_position}")

        return final_position

    def print_board(self, players: Deque[Player]) -> None:
        print("\nCurrent Board State:")

        for i in range(self._side_length):
            for j in range(self._side_length):
                position = self._grid[i][j].position
                cell_content = str(position)

                if self._grid[i][j].has_obstacle():
                    obstacle = self._grid[i][j].obstacle
                    if obstacle.get_obstacle_type() == ObstacleType.SNAKE:
                        cell_content = f"🐍{obstacle.dest}"
                    else:
                        cell_content = f"🪜{obstacle.dest}"

                for player in players:
                    if player.position == position:
                        cell_content = player.name

                print(f"{cell_content:<8}", end="")
            print()
        print()
