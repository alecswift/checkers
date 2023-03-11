from __future__ import annotations
from enum import Enum
from typing import Tuple


def main():
    game = Checkers()
    player_1 = game.create_player("p2", "Black")
    player_2 = game.create_player("p1", "White")
    game.play_game(player_1.get_player_name(), (2, 5), (1, 4))
    game.print_board()
    game.play_game(player_2.get_player_name(), (5, 2), (4, 3))
    game.play_game(player_1.get_player_name(), (3, 6), (2, 5))
    game.play_game(player_2.get_player_name(), (4, 3), (3, 4))
    game.play_game(player_1.get_player_name(), (6, 5), (7, 4))
    game.play_game(player_2.get_player_name(), (6, 1), (5, 2))
    game.print_board()
    game.play_game(player_1.get_player_name(), (2, 5), (6, 1))
    game.print_board()

Pos = tuple[int, int]

class Checkers:
    """Represents a game of checkers between two players
    objects with the checker board as a data member"""

    def __init__(self):
        self._board: dict[str, str] = {}  # position: status
        # more stylish way of doing this?
        self.init_board()
        self._players = {}  # Name: player object
        self._turn = 0
        self._curr_player = None

    def get_board(self):
        """Returns the board data member"""
        return self._board

    def get_players(self):
        """Returns the players data member"""
        return self._players

    def get_turn(self):
        """Returns the turn data member"""
        return self._turn

    def init_board(self):
        """Initialize the starting board state"""
        for x_coord in range(8):
            for y_coord in range(8):
                # could set this conditional to continue the loop
                # if no need for None space
                if (x_coord + y_coord) % 2 == 0:
                    self._board[(x_coord, y_coord)] = None
                elif y_coord in (0, 1, 2):
                    self._board[(x_coord, y_coord)] = "White"
                elif y_coord in (3, 4):
                    self._board[(x_coord, y_coord)] = "Empty"
                else:
                    self._board[(x_coord, y_coord)] = "Black"

    def create_player(self, name: str, piece_color: str) -> Player:
        """
        Creates a returns a player object from the given player name
        and chosen piece color
        """
        new_player = Player(name, piece_color)
        self._players[name] = new_player
        new_player.set_checkers_game(self)
        return new_player

    def play_game(self, name: str, start_pos: Pos, dest_pos: Pos) -> int:
        """
        Returns the number of pieces captured and moves the checker piece
        on the board from a given player name, starting square position,
        and destination square position
        """
        player = self._players.get(name)
        self.invalid_moves(player, start_pos, dest_pos)
        self._turn += 1
        val = self._board[start_pos]
        root_node = PathNode(start_pos, val)
        self._curr_player = player
        self.rec_play_game(root_node, dest_pos)
        self._board[dest_pos] = val

    def invalid_moves(self, player: Player, start_pos: Pos, dest_pos: Pos) -> str:
        """
        Raises exceptions for invalid player, a player trying to play out of turn,
        and an invalid move that is the wrong piece or is outside of the board
        """
        if player is None:
            raise InvalidPlayer
        if player.get_checker_color() == "Black" and self._turn % 2 == 1:
            raise OutofTurn
        if player.get_checker_color() == "White" and self._turn % 2 == 0:
            raise OutofTurn
        piece = self._board.get(start_pos)
        end_space = self._board.get(dest_pos)
        if piece is None or player.get_checker_color() not in piece:
            raise InvalidSquare
        if end_space is None:
            raise InvalidSquare

    def rec_play_game(self, curr_node: PathNode, dest_pos: Pos) -> int:
        """Recursively executes a player's checker move"""
        pos = curr_node.pos
        if pos == dest_pos:
            self.modify_board(curr_node)
            return
        color = self._curr_player.get_checker_color()
        right_move = Direction.UP_RIGHT.move(pos, color)
        left_move = Direction.UP_LEFT.move(pos, color)
        self.handle_moves(curr_node, Direction.UP_RIGHT, right_move, dest_pos)
        self.handle_moves(curr_node, Direction.UP_LEFT, left_move, dest_pos)

    def handle_moves(self, node: PathNode, direct: Tuple, move: Pos, dest: Pos) -> None:
        """
        Decide whether or not the current move is a jump, then call
        the rec_play_game function with the correct node
        """
        val = self._board.get(move)
        color = self._curr_player.get_checker_color()
        opp_color = "Black" if color == "White" else "White"
        next_node = PathNode(move, val, node)
        first_move: bool = node.parent is None
        if val is not None and opp_color in val:
            jump = direct.move(move, color)
            if self._board.get(jump) == "Empty":
                jump_node = PathNode(jump, self._board[jump], next_node)
                return self.rec_play_game(jump_node, dest)
        elif val == "Empty" and first_move:
            return self.rec_play_game(next_node, dest)

    def modify_board(self, curr_node: PathNode) -> None:
        """Modify the board based on the given PathNode of the player's move"""
        while curr_node is not None:
            if curr_node.val != "Empty":
                self._board[curr_node.pos] = "Empty"
            curr_node = curr_node.parent

    def get_checker_details(self, square_pos: Pos):
        """Returns the checker details from the given square location"""
        piece = self._board.get(square_pos, "off_board")
        if piece == "off_board":
            raise InvalidSquare
        if piece is None or piece == "Empty":
            return None
        return piece

    def print_board(self) -> None:
        """Prints the current checker board as an array"""
        board_array = [[None] * 8 for _ in range(8)]
        for pos, val in self._board.items():
            x_coord, y_coord = pos
            board_array[y_coord][x_coord] = val
        print(end="  ")
        for num in range(8):
            print(f" {num}", end="")
        print()
        for idx, row in enumerate(board_array):
            print(idx, end=" ")
            for val in row:
                if val in (None, "Empty"):
                    print("| ", end="")
                elif "W" in val:
                    print("|w", end="")
                else:
                    print("|b", end="")
            print("|")

    def game_winner(self) -> str:
        """Returns the winner of the checker game"""


class Player:
    """
    Represents a player in a game of checkers with the
    data members player name and checker color
    """

    def __init__(self, player_name: str, checker_color: str):
        self._player_name = player_name
        self._checker_color = checker_color
        self._captured_pieces_count = 0
        self._checkers_game = None

    def get_player_name(self) -> None:
        """Return the players name"""
        return self._player_name

    def get_checker_color(self) -> None:
        """Return the players checker color"""
        return self._checker_color

    def set_checkers_game(self, checkers_game: Checkers) -> None:
        """Sets the players board to the given board"""
        self._checkers_game = checkers_game

    # Add tests for king count methods
    def get_king_count(self) -> int:
        """Returns the number of kings the player has"""
        return self.count("_king")

    def get_triple_king_count(self) -> int:
        """Returns the number of triple kings the player has"""
        return self.count("_Triple_king")

    def count(self, type_of_king: str) -> int:
        """
        Returns the number of the given type of king that the player has
        """
        board = self._checkers_game.get_board()
        target = f"{self._checker_color}{type_of_king}"
        return sum(1 for val in board.values() if val == target)

    def get_captured_pieces_count(self) -> int:
        """
        returns the number of opponent pieces that
        the player has captured
        """
        return self._captured_pieces_count


class OutofTurn(Exception):
    """
    User defined exception if a player trys to play checkers
    out of turn
    """


class InvalidSquare(Exception):
    """
    User defined exception if a player trys to access an
    invalid square for their start position in checkers
    """


class InvalidPlayer(Exception):
    """
    User defined exception if a player name does not
    exist for the current game of checkers
    """


class PathNode:
    """Represents a node in the path of a checker move"""

    def __init__(self, pos, val, parent=None):
        self.pos = pos
        self.val = val
        self.parent = parent


class Direction(Enum):
    """Represents all the directions a checker piece can move"""

    UP_LEFT = ((-1, -1), (1, 1))
    UP_RIGHT = ((1, -1), (-1, 1))
    DOWN_LEFT = ((-1, 1), (1, -1))
    DOWN_RIGHT = ((1, 1), (-1, -1))

    def move(self, pos, color) -> tuple[int, int]:
        """Move a checker piece of a given position and color"""
        idx = 0 if color == "Black" else 1
        x_coord, y_coord = pos
        move_x, move_y = self.value[idx]
        return (x_coord + move_x, y_coord + move_y)


if __name__ == "__main__":
    main()
