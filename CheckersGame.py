from __future__ import annotations
from enum import Enum
from itertools import product


def main():
    pass

Pos = complex
Path = tuple[complex]

class Checkers:
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
            if (x_coord + y_coord) % 2 == 0: # Invalid squares
                self._board[coord] = None
            elif y_coord in (0, 1, 2):
                self._board[coord] = Piece(coord, 'white')
            elif y_coord in (3, 4):
                self._board[coord] = 'empty'
            else:
                self._board[coord] = Piece(coord, 'black')

    def valid_paths(self, player: Player) -> list[Path]:
        paths = []
        for piece in player.pieces:
            forward_left = Direction.FORWARD_LEFT.move(piece.pos, piece.color)
            forward_right = Direction.FORWARD_RIGHT.move(piece.pos, piece.color)
            # rather than if chain send each direction to a function
            self.handle_moves()

    def handle_moves(self, curr_path, piece, first_move, paths):
        # consider changing to tree?
        *rest, curr_pos, next_pos = curr_path
        next_val = self._board[next_pos]
        opp_color = 'black' if piece.color == 'white' else 'black'
        if next_val is None:
            return
        if next_val == "empty" and not first_move:
            path = *rest, curr_pos
            paths.append(path)
            return
        if next_val == "empty":
            paths.append((piece.pos, next_pos))
            return
        elif opp_color in next_val.color:
            # if next move is empty check make new curr_path with possible directions
            # call handle moves with each of these paths
            # remember kings can move backwards but not back into the prev position
            move = next_pos - curr_pos
            jump = next_pos + move
            if self._board[next_pos + move] == "empty":
                forward_left = Direction.FORWARD_LEFT.move(jump, piece.color)
                forward_right = Direction.FORWARD_RIGHT.move(jump, piece.color)
                left_path = *rest, curr_pos, next_pos, jump, forward_left
                right_path = *rest, curr_pos, next_pos, jump, forward_right
                first_move = False
                self.handle_moves(left_path, piece, first_move, paths)
                self.handle_moves(right_path, piece, first_move, paths)



class Player:
    """
    Represents a player in a game of checkers with the
    data members player name and checker color
    """

    def __init__(self, checker_color: str, checkers_game: Checkers):
        self._checker_color = checker_color
        self._checkers_game = checkers_game
        self._pieces: list[Piece] = []
        self._init_pieces
        self._captured_pieces: int = 0
    
    def init_pieces(self) -> None:
        """Adds the players pieces of the appropriate color to the pieces data member"""
        for piece in self._checkers_game.board.values():
            if self._checker_color in piece.val:
                self._pieces.append(piece)

    @property
    def pieces(self) -> list[Piece]:
        return self._pieces

    @property
    def captured_pieces(self) -> int:
        """
        returns the number of opponent pieces that
        the player has captured
        """
        return self._captured_pieces_count


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
        self.rank = 'man'

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

    FORWARD_LEFT = (-1-1j, 1+1j)
    FORWARD_RIGHT = (1-1j, -1+1j)
    BACK_LEFT = (-1+1j, 1-1j)
    BACK_RIGHT = (1+1j, -1-1j)

    def move(self, pos, color) -> tuple[int, int]:
        """Move a checker piece of a given position and color"""
        idx = 0 if color == 'black' else 1
        move = self.value[idx]
        return pos + move


if __name__ == "__main__":
    main()
