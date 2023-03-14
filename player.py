from __future__ import annotations
from enum import Enum
from board import Board, Piece

Pos = complex
Path = tuple[complex]


class Player:
    """
    Represents a player in a game of checkers with the
    data members player name and checker color
    """

    def __init__(self, checker_color: str, board: Board):
        self._color = checker_color
        self._board = board
        self._pieces: list[Piece] = set()
        self.init_pieces()

    def init_pieces(self) -> None:
        """Adds the players pieces of the appropriate color to the pieces data member"""
        for piece in self.board.values():
            is_player_piece = isinstance(piece, Piece) and self._color == piece.color
            if is_player_piece:
                self._pieces.add(piece)

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

    def potential_paths(self) -> list[Path]:
        """
        Returns all possible paths that a given player can take with
        their current pieces
        """
        paths = []
        for piece in self._pieces:
            path = (piece.pos,)
            capture = False
            self.build_path_1(path, paths, piece, capture)
        return paths
    
    def build_path_1(self, path, paths, piece, capture):
        *_, curr_pos = path
        forward_left = Direction.FORWARD_LEFT.move(curr_pos, piece.color)
        forward_right = Direction.FORWARD_RIGHT.move(curr_pos, piece.color)
        left_path = *path, forward_left
        right_path = *path, forward_right
        self.build_path(left_path, piece, capture, paths)
        self.build_path(right_path, piece, capture, paths)
        if piece.rank == "king":
            pass

    def build_path(
        self, curr_path: Path, piece: Piece, capture: bool, paths: list[Path]
    ) -> None:
        """
        Recursive function that builds all possible paths from the given first
        two moves in curr_path and adds each path to the paths list
        """
        # should refactor logic here
        *rest, curr_pos, next_pos = curr_path
        next_val = self.board.get(next_pos)
        color = piece.color
        opp_color = "black" if color == "white" else "white"
        if not capture and next_val == "empty":
            paths.append(curr_path)
            return
        if not capture and next_val is None:
            return
        if capture and next_val == "empty":
            paths.append((*rest, curr_pos))
            return
        if capture and next_val is None:
            paths.append((*rest, curr_pos))
            return
        if next_val.color == opp_color:
            move = next_pos - curr_pos
            jump = next_pos + move
            if self.board.get(jump) == "empty":
                self.build_path_1((*curr_path, jump), paths, piece , True)
            elif capture:
                paths.append((*rest, curr_pos))

    def prune_paths(self, paths):
        max_length = max(len(path) for path in paths)
        return [path for path in paths if len(path) == max_length]

    def no_capture_move(self, start_pos: complex, end_pos: complex) -> None:
        piece = self.board[start_pos]
        self.board[start_pos] = "empty"
        self.board[end_pos] = piece
        piece.pos = end_pos

    def capture_move(self, path, opponent):
        start_pos, opp_pos, end_pos, *rest = path
        self.no_capture_move(start_pos, end_pos)
        opp_piece = self.board[opp_pos]
        opponent.pieces.remove(opp_piece)
        self.board[opp_pos] = "empty"
        new_path = end_pos, *rest
        return new_path


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
