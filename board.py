from __future__ import annotations
from itertools import product
from typing import Optional

Pos = complex


class Piece:
    """
    Represents a piece in a checker game. Utilized as a struct so that
    when a piece is promoted or moved the piece changes in both the
    player pieces data member and the Checkers board data member
    """

    def __init__(self, pos: Pos, color: str):
        self.pos = pos
        self.color = color
        self.rank: str = "man"


BoardDict = dict[complex, str | Piece | None]


class Board:
    """Represents a game of checkers between two players
    objects with the checker board as a data member"""

    def __init__(self):
        self._board: BoardDict = {}  # position: status
        self.init_board()

    @property
    def board(self) -> BoardDict:
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

    def board_array(self) -> list[list[Optional[str]]]:
        """Returns the checker board in the form of an array"""
        board_array = [[None] * 8 for _ in range(8)]
        for pos, piece in self._board.items():
            if isinstance(piece, Piece):
                pos = piece.pos
                x_coord, y_coord = int(pos.real), int(pos.imag)
                val = piece.color
                board_array[y_coord][x_coord] = val
        return board_array

    def print_board(self) -> None:
        """Prints the current checker board as an array"""
        print(self.board_array())

    def __str__(self) -> str:
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
                    board_str.append("| w")
                else:
                    board_str.append("| b")
            board_str.append("|\n")
        return "".join(board_str)
