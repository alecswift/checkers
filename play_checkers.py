from os import system
from time import sleep
from checkers import Checkers, InvalidPlayer, InvalidSquare, OutofTurn

def play():
    game = Checkers()
    p1 = game.create_player("p2", "Black")
    p2 = game.create_player("p1", "White")
    while True:
        game.print_board()
        player = p1 if game.get_turn() % 2 == 0 else p2
        print(f"{player.get_checker_color()} make your move")
        start_x = int(input("Column of start location: "))
        start_y = int(input("Row of start location: "))
        end_x = int(input("Column of end location: "))
        end_y = int(input("Row of end location: "))
        try:
            game.play_game(player.get_player_name(), (start_x, start_y), (end_x, end_y))
        except InvalidPlayer:
            print("That is not a valid player")
        except InvalidSquare:
            print("That is not a valid location")
        except OutofTurn:
            print("It is not your turn")
        finally:
            sleep(2)
            system("clear")

if __name__ == "__main__":
    play()
