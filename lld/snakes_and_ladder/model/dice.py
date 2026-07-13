import random


class Dice:
    def __init__(self, no_of_dices: int) -> None:
        self._no_of_dices = no_of_dices
        self._random = random.Random()

    def roll(self) -> int:
        total = 0
        for _ in range(self._no_of_dices):
            total += self._random.randint(1, 6)
        return total
