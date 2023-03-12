from __future__ import annotations
from enum import Enum
from itertools import product


def main():
    pass


Pos = complex
Path = tuple[complex]


class Board:
    """Represents a game of checkers between two players
    objects with the checker board as a data member"""

    def __init__(self):
        self._board: dict[str, str] = {}  # position: status
        self.init_board()

    @property
    def board(self) -> dict[str, str]:
        """Returns the board data member"""
        return self._board

    def init_board(self) -> None:
        """Initialize the starting board state"""
        for x_coord, y_coord in product(range(8), range(8)):
            coord = complex(x_coord, y_coord)
            if (x_coord + y_coord) % 2 == 0:  # Invalid squares
                self._board[coord] = None
            elif y_coord in (0, 1, 2):
                self._board[coord] = Piece(coord, "white")
            elif y_coord in (3, 4):
                self._board[coord] = "empty"
            else:
                self._board[coord] = Piece(coord, "black")

    def board_array(self):
        """Returns the checker board in the form of an array"""
        board_array = [[None] * 8 for _ in range(8)]
        for pos, piece in self._board.items():
            if piece not in (None, "empty"):
                x_coord, y_coord = int(pos.real), int(pos.imag)
                val = piece.color
                board_array[y_coord][x_coord] = val
        return board_array

    def print_board(self):
        """Prints the current checker board as an array"""
        print(self.board_array())

    def __str__(self):
        """Returns the string version of the checker board for debugging"""
        board_array = self.board_array()
        board_str = ["  "]
        for num in range(8):
            board_str.append(f"  {num}")
        board_str.append("\n")
        for idx, row in enumerate(board_array):
            board_str.append(f"{idx} ")
            for val in row:
                if val is None:
                    board_str.append("|  ")
                elif "white" in val:
                    if "Triple_King" in val:
                        board_str.append("|WT")
                    elif "king" in val:
                        board_str.append("| W")
                    else:
                        board_str.append("| w")
                else:
                    if "Triple_King" in val:
                        board_str.append("|BT")
                    elif "king" in val:
                        board_str.append("| B")
                    else:
                        board_str.append("| b")
            board_str.append("|\n")
        return "".join(board_str)


class Player:
    """
    Represents a player in a game of checkers with the
    data members player name and checker color
    """

    def __init__(self, checker_color: str, board: Board):
        self._color = checker_color
        self._board = board
        self._pieces: list[Piece] = []
        self.init_pieces()
        self._captured_pieces: int = 0

    def init_pieces(self) -> None:
        """Adds the players pieces of the appropriate color to the pieces data member"""
        for piece in self.board.values():
            is_player_piece = piece not in (None, "empty") and self._color == piece.color
            if is_player_piece:
                self._pieces.append(piece)

    @property
    def pieces(self) -> list[Piece]:
        return self._pieces

    @property
    def board(self) -> dict:
        return self._board.board

    @property
    def captured_pieces(self) -> int:
        """
        returns the number of opponent pieces that
        the player has captured
        """
        return self._captured_pieces_count

    def valid_paths(self) -> list[Path]:
        """
        Returns all possible paths that a given player can take with
        their current pieces
        """
        paths = []
        for piece in self._pieces:
            pos = piece.pos
            color = piece.color
            forward_left = Direction.FORWARD_LEFT.move(pos, color)
            forward_right = Direction.FORWARD_RIGHT.move(pos, color)
            # rather than if chain send each direction to a function
            self.handle_moves((pos, forward_left), piece, True, paths)
            self.handle_moves((pos, forward_right), piece, True, paths)
            if piece.rank == "king":
                pass
        return paths

    def handle_moves(
        self, curr_path: Path, piece: Piece, first_move: bool, paths: list[Path]
    ) -> None:
        """
        Recursive function that builds all possible paths from the given first
        two moves in curr_path and adds each path to the paths list
        """
        *rest, curr_pos, next_pos = curr_path
        next_val = self.board.get(next_pos)
        color = piece.color
        opp_color = "black" if color == "white" else "white"
        if next_val is None:
            return
        if next_val == "empty" and not first_move:
            path = *rest, curr_pos
            paths.append(path)
            return
        if next_val == "empty":
            paths.append(curr_path)
            return
        if next_val.color == opp_color:
            move = next_pos - curr_pos
            jump = next_pos + move
            if self.board.get(jump) == "empty":
                forward_left = Direction.FORWARD_LEFT.move(jump, color)
                forward_right = Direction.FORWARD_RIGHT.move(jump, color)
                left_path = *curr_path, jump, forward_left
                right_path = *curr_path, jump, forward_right
                first_move = False
                self.handle_moves(left_path, piece, first_move, paths)
                self.handle_moves(right_path, piece, first_move, paths)


class Piece:
    """
    Represents a piece in a checker game. Utilized as a struct so that
    when a piece is promoted or moved the piece changes in both the
    player pieces data member and the Checkers board data member
    """

    # One drawback to consider is the redundancy in the board data member
    # both the key and value contain the position

    def __init__(self, pos: Pos, color):
        self.pos = pos
        self.color = color
        self.rank = "man"


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


class Direction(Enum):
    """Represents all the directions a checker piece can move"""

    FORWARD_LEFT = (-1 - 1j, 1 + 1j)
    FORWARD_RIGHT = (1 - 1j, -1 + 1j)
    BACK_LEFT = (-1 + 1j, 1 - 1j)
    BACK_RIGHT = (1 + 1j, -1 - 1j)

    def move(self, pos, color) -> tuple[int, int]:
        """Move a checker piece of a given position and color"""
        idx = 0 if color == "black" else 1
        move = self.value[idx]
        return pos + move


if __name__ == "__main__":
    main()
