from __future__ import annotations
from enum import Enum, Flag, auto
from itertools import product
from typing import Optional

Pos = complex
Path = tuple[complex, ...]
BoardState = tuple[tuple[complex, int]]


def init_state() -> BoardState:
    state = []
    for x_coord, y_coord in product(range(8), range(8)):
        pos = complex(x_coord, y_coord)
        if (x_coord + y_coord) % 2 == 0:  # Invalid squares
            continue
        elif y_coord in (0, 1, 2):
            state.append((pos, Piece.WHITE))
        elif y_coord in (3, 4):
            state.append((pos, Piece.EMPTY))
        else:
            state.append((pos, Piece.BLACK))
    return tuple(state)


def init_borders():
    """Return a set of border coordinates for a checkers board"""
    borders = set()
    borders_nums = [-1, 8]
    for num1 in borders_nums:
        for num2 in range(0, 7):
            borders.add(complex(num1, num2))
            borders.add(complex(num2, num1))
    return borders


class Board:
    def __init__(self, board_state, borders):
        self._board_state = board_state
        self._borders = borders

    def find_valid_moves(self, max_player) -> list[Path]:
        moves = set()
        color = Piece.WHITE if max_player else Piece.BLACK
        for pos, piece in self._board_state:
            if color in piece:
                captures = 0
                skips = ()
                positions = (None, pos)
                move = (piece, positions, skips, captures)
                self.next_move(move, moves)
        valid_moves = self.prune_moves(moves)
        return valid_moves

    def next_move(self, move: Path, moves: list[Path]) -> None:
        piece, positions, skips, captures = move
        *_, prev_pos, curr_pos = positions
        forward_left = Direction.FORWARD_LEFT.move(curr_pos, piece)
        forward_right = Direction.FORWARD_RIGHT.move(curr_pos, piece)
        next_positions = [forward_left, forward_right]

        if Piece.KING not in piece:
            for next_pos in next_positions:
                next_move = (piece, (*positions, next_pos), skips, captures)
                self.build_path(next_move, moves)
        else:
            back_left = Direction.BACK_LEFT.move(curr_pos, piece)
            back_right = Direction.BACK_RIGHT.move(curr_pos, piece)
            next_positions.extend([back_left, back_right])
            for next_pos in next_positions:
                if next_pos == prev_pos:
                    continue
                next_move = (piece, (*positions, next_pos), skips, captures)
                self.build_path(next_move, moves)

    def build_path(self, move: Path, moves: list[Path]) -> None:
        # Check if I really need the piece in the path
        piece, positions, skips, captures = move
        prev, *rest, curr_pos, next_pos = positions
        next_val = self.search_state(next_pos)
        next_val_is_empty = next_val == Piece.EMPTY
        opp_color = Piece.BLACK if Piece.WHITE in piece else Piece.WHITE
        color = Piece.BLACK if Piece.BLACK in piece else Piece.WHITE

        if not captures and next_val_is_empty:
            moves.add((piece, (*rest, curr_pos, next_pos), skips, captures))
        elif captures and next_val is None:
            moves.add((piece, (*rest, curr_pos), skips, captures))
        # next one could be faulty
        elif captures and (color in next_val or next_val_is_empty):
            moves.add((piece, (*rest, curr_pos), skips, captures))
        elif isinstance(next_val, Piece) and next_val in opp_color:
            move = next_pos - curr_pos
            jump = next_pos + move
            jump_val = self.search_state(jump)
            if jump_val == Piece.EMPTY:
                positions = (prev, *rest, curr_pos, jump)
                skips = (*skips, next_pos)
                jmp_move = (piece, positions, skips, captures + 1)
                self.next_move(jmp_move, moves)
            elif captures:
                moves.add((piece, (*rest, curr_pos), skips, captures))

    def search_state(self, next_pos):
        for pos, val in self._board_state:
            if pos == next_pos:
                next_val = val
                break
        else:
            next_val = None
        return next_val

    def prune_moves(self, moves) -> list[Path]:
        """
        Removes all invalid moves from the given moves list. A path is invalid if
        there is another path in the list with more captures
        """
        if moves:
            max_captures = max(captures for _, _, _, captures in moves)
            moves = set(
                (piece, positions, skips)
                for piece, positions, skips, captures in moves
                if captures == max_captures
            )
        return moves

    def __str__(self) -> str:
        """Returns the string version of the checker board for debugging"""
        board_array = [[None] * 8 for _ in range(8)]
        for pos, piece in self._board_state:
            if piece != Piece.EMPTY:
                x_coord, y_coord = int(pos.real), int(pos.imag)
                val = "black" if piece == Piece.BLACK else "white"
                board_array[y_coord][x_coord] = val

        board_str = []
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


class Piece(Flag):

    """Represents a checker piece"""

    EMPTY = auto()
    WHITE = auto()
    BLACK = auto()
    KING = auto()
    WHITE_KING = WHITE | KING
    BLACK_KING = BLACK | KING

class Direction(Enum):
    """
    Represents all the directions a checker piece can move
    The 0 index of the direction tuples represents black piece
    moves and the 1 index represents white piece moves
    """

    FORWARD_LEFT = (-1 - 1j, 1 + 1j)
    FORWARD_RIGHT = (1 - 1j, -1 + 1j)
    BACK_LEFT = (-1 + 1j, 1 - 1j)
    BACK_RIGHT = (1 + 1j, -1 - 1j)

    def move(self, pos: Pos, piece: Piece) -> complex:
        """Move a checker piece of a given position and color"""
        # Possibly better way to interconnect piece and direction?
        idx = 0 if Piece.BLACK in piece else 1
        move = self.value[idx]
        return pos + move
