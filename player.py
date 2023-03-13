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
        self._pieces: list[Piece] = [] # possibly change to set
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
            self.build_paths((pos, forward_left), piece, True, paths)
            self.build_paths((pos, forward_right), piece, True, paths)
            if piece.rank == "king":
                pass
        return paths

    def build_paths(
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
                self.build_paths(left_path, piece, first_move, paths)
                self.build_paths(right_path, piece, first_move, paths)
    
    def no_capture_move(self, path: Path):
        start_pos, end_pos = path
        piece = self.board[start_pos]
        self.board[start_pos] = "empty"
        self.board[end_pos] = piece
        piece.pos = end_pos

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