from .model.player import Player
from .service.game import Game


def main() -> None:
    board_size = int(input("Enter the board size : "))
    no_of_snakes = int(input("Enter the number of snakes : "))
    no_of_ladders = int(input("Enter the number of ladders : "))
    no_of_players = int(input("Enter the number of players : "))
    no_of_dice = int(input("Enter the number of Dice : "))

    game = Game(board_size, no_of_ladders, no_of_snakes, no_of_dice)

    for i in range(no_of_players):
        name = input(f"Enter the name of player {i + 1} : ")
        player = Player(name)
        game.add_player(player)

    game.start_game()


if __name__ == "__main__":
    main()
