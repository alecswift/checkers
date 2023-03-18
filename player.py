from __future__ import annotations
from enum import Enum
from board import Board, Piece, Pos, BoardDict

Path = tuple[complex, ...]


class Player:
    """
    Represents a player in a game of checkers with the
    data members player name and checker color
    """

    def __init__(self, checker_color: str, board: Board):
        self._color = checker_color
        self._board = board
        self._pieces: set[Piece] = set()
        self.init_pieces()

    def init_pieces(self) -> None:
        """Adds the players pieces of the appropriate color to the pieces data member"""
        for piece in self.board.values():
            if isinstance(piece, Piece) and self._color == piece.color:
                self._pieces.add(piece)

    @property
    def color(self) -> str:
        return self._color

    @property
    def board(self) -> BoardDict:
        return self._board.board

    @property
    def pieces(self) -> set[Piece]:
        return self._pieces

    def valid_paths(self) -> list[Path]:
        """
        Returns all possible paths that a given player can take with
        their current pieces
        """
        paths: list[Path] = []
        for piece in self._pieces:
            path = (piece.pos,)
            capture = False
            self.next_move(path, paths, piece, capture)
        paths = self.prune_paths(paths)
        return paths

    def next_move(
        self, path: Path, paths: list[Path], piece: Piece, capture: bool
    ) -> None:
        """
        Finds the next possible move and calls build path with the given
        path, piece, and capture bool
        """
        if not capture:
            prev_pos = None
            *_, curr_pos = path
        else:
            *_, prev_pos, curr_pos = path
        forward_left = Direction.FORWARD_LEFT.move(curr_pos, piece.color, "black")
        forward_right = Direction.FORWARD_RIGHT.move(curr_pos, piece.color, "black")
        next_positions = [forward_left, forward_right]
        if piece.rank != "king":
            for next_position in next_positions:
                next_path = *path, next_position
                self.build_path(next_path, piece, capture, paths)
        else:
            back_left = Direction.BACK_LEFT.move(curr_pos, piece.color, "black")
            back_right = Direction.BACK_RIGHT.move(curr_pos, piece.color, "black")
            next_positions.extend([back_left, back_right])
            for next_position in next_positions:
                if prev_pos == next_position:
                    continue
                next_path = *path, next_position
                self.build_path(next_path, piece, capture, paths)

    def build_path(
        self, path: Path, piece: Piece, capture: bool, paths: list[Path]
    ) -> None:
        """
        Recursive function that builds all possible paths from the given first
        two moves in path and adds each path to the paths list

        cases for valid paths:
        It's the first move (not capture) and the next space is empty.
        Or anytime after a capture move where the next space is not an
        opponent piece. If the next space is an opponents piece trigger
        a recursive call if the space the piece would jump to is empty.
        """
        *rest, curr_pos, next_pos = path
        next_val = self.board.get(next_pos)
        color = piece.color
        opp_color = "black" if color == "white" else "white"

        if not capture and next_val == "empty":
            paths.append(path)
        elif capture and not isinstance(next_val, Piece):
            paths.append((*rest, curr_pos))
        elif capture and isinstance(next_val, Piece) and next_val.color == color:
            paths.append((*rest, curr_pos))
        elif isinstance(next_val, Piece) and next_val.color == opp_color:
            move = next_pos - curr_pos
            jump = next_pos + move
            if self.board.get(jump) == "empty":
                self.next_move((*path, jump), paths, piece, True)
            elif capture:
                paths.append((*rest, curr_pos))

    def prune_paths(self, paths: list[Path]) -> list[Path]:
        """
        Removes all invalid paths from the given paths list. A path is invalid if
        there is another path in the list with more captures
        """
        if paths:
            max_length = max(len(path) for path in paths)
            return [path for path in paths if len(path) == max_length]
        return paths

    def no_capture_move(self, start_pos: complex, end_pos: complex) -> None:
        """
        Carries out a checker move involving no captures from the
        given start and end positions
        """
        piece = self.board[start_pos]
        assert isinstance(piece, Piece)
        self.board[start_pos] = "empty"
        self.board[end_pos] = piece
        piece.pos = end_pos
        if piece.rank == "man":
            self.handle_promotion(piece)

    def capture_move(self, path: Path, opponent: Player) -> Path:
        """
        Carries out a checker move involving one or more captures from the
        given path and player opponent. Returns the remaining path if there
        are more than one captures
        """
        start_pos, opp_pos, end_pos, *rest = path
        piece = self.board[start_pos]
        assert isinstance(piece, Piece)
        self.no_capture_move(start_pos, end_pos)

        opp_piece = self.board[opp_pos]
        assert isinstance(opp_piece, Piece)
        opponent.pieces.remove(opp_piece)
        self.board[opp_pos] = "empty"
        new_path = end_pos, *rest

        if piece.rank == "man":
            self.handle_promotion(piece)
        return new_path
    
    def ai_capture_move(self, path, opponent):
        start_pos, *rest, end_pos = path
        piece = self.board[start_pos]
        assert isinstance(piece, Piece)
        self.no_capture_move(start_pos, end_pos)
        for idx, opp_pos in enumerate(rest):
            if idx % 2 == 0:
                opp_piece = self.board[opp_pos]
                assert isinstance(opp_piece, Piece)
                opponent.pieces.remove(opp_piece)
                self.board[opp_pos] = "empty"
        if piece.rank == "man":
            self.handle_promotion(piece)



    def handle_promotion(self, piece: Piece):
        """Promotes a piece to king if it lands on the row opposite of the start"""
        promotion_row = 0 if piece.color == "black" else 7
        curr_row = piece.pos.imag
        if curr_row == promotion_row:
            piece.rank = "king"


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

    def move(self, pos: Pos, color: str, color_type: str | int) -> complex:
        """Move a checker piece of a given position and color"""
        idx = 0 if color == color_type else 1
        move = self.value[idx]
        return pos + move
