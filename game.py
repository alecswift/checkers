from __future__ import annotations
from enum import Enum, Flag, auto
from itertools import product

Pos = complex
Path = tuple[complex, ...]
BoardState = tuple[tuple[complex, int]]



def get_moves_from(color, start_pos, state_obj):
    moves = []
    for piece, positions, skips in state_obj.find_valid_moves(color):
        curr_start, curr_end, *_ = positions
        captures = len(skips)
        if captures:
            skips = (skips[0],)
        if curr_start == start_pos:
            moves.append((piece, (curr_start, curr_end), skips, captures))
    return moves

def make_move(move, state):
    #Change to take one jump at a time except for in the minimax algo
    piece, positions, skips = move
    start_pos, *_, end_pos = positions
    remove = set([start_pos, end_pos])
    removed = tuple((pos, val) for pos, val in state if pos not in remove)
    removed_opp = tuple(
            (pos, Piece.EMPTY) if pos in skips else (pos, val) for pos, val in removed
        )
    if Piece.KING not in piece:
        piece = handle_promotion(end_pos.imag, piece)
    new_state = *removed_opp, (end_pos, piece), (start_pos, Piece.EMPTY)
    return new_state


def handle_promotion(row, piece):
    promotion_row = 7 if piece == Piece.WHITE else 0
    if promotion_row == row:
        return Piece.BLACK_KING if piece == Piece.BLACK else Piece.WHITE_KING
    return piece

def game_won(state):
    """Return if the checkers game has been won from the given board state"""



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

    @property
    def board_state(self):
        return self._board_state

    @board_state.setter
    def board_state(self, new_state):
        self._board_state = new_state


    def find_valid_moves(self, color) -> list[Path]:
        moves = set()
        for pos, piece in self._board_state:
            if color in piece:
                captures = 0
                skips = ()
                positions = (pos,)
                move = (piece, positions, skips, captures)
                self.next_move(move, moves)
        valid_moves = self.prune_moves(moves)
        return valid_moves

    def next_move(self, move: Path, moves: list[Path], prev_pos=None) -> None:
        piece, positions, skips, captures = move
        *_, curr_pos = positions
        forward_left = Direction.FORWARD_LEFT.move(curr_pos, piece)
        forward_right = Direction.FORWARD_RIGHT.move(curr_pos, piece)
        next_positions = [forward_left, forward_right]

        if Piece.KING not in piece:
            for next_pos in next_positions:
                next_move = (piece, (*positions, next_pos), skips, captures)
                self.build_path(next_move, moves, prev_pos)
        else:
            back_left = Direction.BACK_LEFT.move(curr_pos, piece)
            back_right = Direction.BACK_RIGHT.move(curr_pos, piece)
            next_positions.extend([back_left, back_right])
            for next_pos in next_positions:
                if next_pos == prev_pos:
                    continue
                next_move = (piece, (*positions, next_pos), skips, captures)
                self.build_path(next_move, moves, prev_pos)

    def build_path(self, move: Path, moves: list[Path], prev_pos) -> None:
        # Check if I really need the piece in the path
        piece, positions, skips, captures = move
        *rest, curr_pos, next_pos = positions
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
        elif isinstance(next_val, Piece) and opp_color in next_val:
            move = next_pos - curr_pos
            jump = next_pos + move
            jump_val = self.search_state(jump)
            if jump_val == Piece.EMPTY:
                positions = (*rest, curr_pos, jump)
                skips = (*skips, next_pos)
                jmp_move = (piece, positions, skips, captures + 1)
                prev = next_pos
                self.next_move(jmp_move, moves, prev)
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
                board_array[y_coord][x_coord] = piece

        board_str = []
        for num in range(8):
            board_str.append(f"  {num}")
        board_str.append("\n")
        for idx, row in enumerate(board_array):
            board_str.append(f"{idx} ")
            for val in row:
                if val == Piece.BLACK:
                    board_str.append("| b")
                elif val == Piece.WHITE:
                    board_str.append("| w")
                elif val == Piece.BLACK_KING:
                    board_str.append("|bk")
                elif val == Piece.WHITE_KING:
                    board_str.append("|wk")
                else:
                    board_str.append("|  ")
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
