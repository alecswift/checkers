from __future__ import annotations
from itertools import product
import pygame


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
                self._board[coord] = Checker(coord, "white")
            elif y_coord in (3, 4):
                self._board[coord] = "empty"
            else:
                self._board[coord] = Checker(coord, "black")

    def board_array(self):
        """Returns the checker board in the form of an array"""
        board_array = [[None] * 8 for _ in range(8)]
        for pos, piece in self._board.items():
            if piece not in (None, "empty"):
                pos = piece.pos
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
    
class BoardImage(Board):
    # possibly combine with board class rather than inheritance?
    def __init__(self, surface, checkers):
        super().__init__()
        self._checkers = checkers  # group of checkers sprites
        self._surface = surface
        self.set_checkers()

    @property
    def checkers(self):
        return self._checkers

    @property
    def surface(self):
        return self._surface

    def set_checkers(self):
        for piece in self.board.values():
            if isinstance(piece, Checker):
                self._checkers.add(piece)

    def display_board(self, screen):
        for x_coord, y_coord in product(range(0, 364, 121), range(0, 364, 121)):
            screen.blit(self._surface, (x_coord, y_coord))


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


class Checker(pygame.sprite.Sprite):
    """moves a clenched fist on the screen, following the mouse"""

    # factor to multiply x and y of the piece, so it is displayed properly on the screen
    COORD_FACTOR = 60.5

    def __init__(self, pos, color):
        super().__init__()
        # messy here fix it up
        self._pos = pos
        self._color = color
        self._rank = "man"
        image_path = f"graphics/{color}_piece.png"
        self.image = pygame.image.load(image_path).convert_alpha()
        # change this to update call elsewhere?
        x_coord, y_coord = int(pos.real), int(pos.imag)
        screen_pos = (x_coord * self.COORD_FACTOR, y_coord * self.COORD_FACTOR)
        self.rect = self.image.get_rect(topleft=(screen_pos))

    @property
    def pos(self):
        return self._pos
    
    @pos.setter
    def pos(self, new_pos):
        self._pos = new_pos

    
    @property
    def color(self):
        return self._color
    
    def rank(self):
        return self._rank

    # https://stackoverflow.com/questions/16825645/how-to-make-a-sprite-follow-your-mouse-cursor-using-pygame
    def update(self):
        """Change the position of the checker based on the piece position data member"""
        x_coord, y_coord = int(self._pos.real), int(self._pos.imag)
        self.rect.topleft = (x_coord * self.COORD_FACTOR, y_coord * self.COORD_FACTOR)

    def update_from_mouse(self):
        "move the checker based on the mouse position"
        # board.board[self._piece.pos] = "empty" # change so it only does this once or impossible?
        # add layering over other checkers
        pos = pygame.mouse.get_pos()
        self.rect.center = pos


if __name__ == "__main__":
    main()
