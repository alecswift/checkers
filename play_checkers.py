# to do
# game logic
# handle capturing moves
# handle piece promotions
# handle game winning conditions (if no valid paths for any pieces game lost)
# handle player switching
# formatting
# possibly reformat class organization (combine Board and board_image?)
# doc strings
# type hinting for function calls
# readme

from itertools import product
import pygame
from sys import exit
from board import Board, Piece
from player import Player


class Checkers:
    def __init__(self):
        self._running = True
        self._screen = None
        self._size = self.weight, self.height = 484, 484
        self._caption = None
        self._board_image = None
        self._board = None
        self._curr_player = None
        self._next_player = None
        self._current_checker = None
        self._capture_path = None

    def on_init(self):
        pygame.init()
        self._screen = pygame.display.set_mode(self._size)
        self._caption = pygame.display.set_caption("Checkers")

        self._board = Board()
        board_surface = pygame.image.load("graphics/chessboard2.png").convert_alpha()
        self._board_image = BoardImage(board_surface, pygame.sprite.Group())
        self._board_image.set_checkers(self._board.board)

        self._curr_player = Player("black", self._board)
        self._next_player = Player("white", self._board)
        self._running = True

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
        if event.type == pygame.MOUSEBUTTONUP:
            self.mouse_button_up()

    def mouse_button_up(self) -> None:
        # improve readability of the logic here with
        # functions and readable bools
        if self._current_checker is None:
            return
        # add player variable for # 2 player
        if self._capture_path is not None:
            # change to paths only from the specific piece?
            valid_paths = [self._capture_path]
            is_capture_move = len(valid_paths[0]) != 2
        else:
            potential_paths = self._curr_player.potential_paths()
            valid_paths = self._curr_player.prune_paths(potential_paths)
            is_capture_move = len(valid_paths[0]) != 2
        for path in valid_paths:
            if is_capture_move:
                start_pos, opp_pos, end_pos, *_ = path
            else:
                start_pos, end_pos = path
            if self._current_checker.pos != start_pos:
                continue
            # could set current paths of piece and iterate through those rather than all paths

            x_coord, y_coord = int(end_pos.real), int(end_pos.imag)
            # middle of end path square
            # function for converting coords from complex to screen coords?
            screen_target = (x_coord * 60.5 + 30.25, y_coord * 60.5 + 30.25)
            pos_selected = self._current_checker.rect.collidepoint(screen_target)
            if not is_capture_move and pos_selected:
                self._curr_player.no_capture_move(start_pos, end_pos)
                self._current_checker.pos = end_pos
                self.switch_player()
            if is_capture_move and pos_selected:
                new_path = self._curr_player.capture_move(path, self._next_player)
                self._current_checker.pos = end_pos
                # remove opponent checker from sprite group make function in boardimage
                for checker in self._board_image.checkers:
                    if checker.pos == opp_pos:
                        checker.kill()
                if 2 < len(new_path):
                    self._capture_path = new_path
                else:
                    self._capture_path = None
                    self.switch_player()
        self._current_checker.update()
        self._current_checker = None

    def switch_player(self):
        self._curr_player, self._next_player = self._next_player, self._curr_player

    def on_input(self):
        mouse_pos = pygame.mouse.get_pos()
        if self._current_checker is not None:
            mouse_pressed, *_ = pygame.mouse.get_pressed()
            if self._current_checker.rect.collidepoint(mouse_pos) and mouse_pressed:
                self._current_checker.update_from_mouse()
        else:
            for checker in self._board_image.checkers:
                mouse_pressed, *_ = pygame.mouse.get_pressed()
                if checker.rect.collidepoint(mouse_pos) and mouse_pressed:
                    self._current_checker = checker
        return self._current_checker

    def on_loop(self):
        pass

    def on_render(self):
        self._board_image.display_board(self._screen)
        self._board_image.checkers.draw(self._screen)
        pygame.display.update()

    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):
        if self.on_init() == False:
            self._running = False

        while self._running:
            for event in pygame.event.get():
                self.on_event(event)
            self.on_input()
            self.on_loop()
            self.on_render()
        self.on_cleanup()


class BoardImage:
    # possibly combine with board class rather than inheritance?
    def __init__(self, surface, checkers):
        super().__init__()
        self._checkers = checkers  # position: CheckerSprite
        self._surface = surface

    @property
    def checkers(self):
        return self._checkers

    @property
    def surface(self):
        return self._surface

    def set_checkers(self, board):
        for pos, piece in board.items():
            if isinstance(piece, Piece):
                self._checkers.add(CheckerSprite(pos, piece.color))

    def display_board(self, screen):
        for x_coord, y_coord in product(range(0, 364, 121), range(0, 364, 121)):
            screen.blit(self._surface, (x_coord, y_coord))


class CheckerSprite(pygame.sprite.Sprite):
    """moves a clenched fist on the screen, following the mouse"""

    # factor to multiply x and y of the piece, so it is displayed properly on the screen
    COORD_FACTOR = 60.5

    def __init__(self, pos, color):
        super().__init__()
        # messy here fix it up
        image_path = f"graphics/{color}_piece.png"
        screen_pos = convert_to_screen_pos(pos)
        self._pos = pos
        self._color = color
        self.image = pygame.image.load(image_path)
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


def convert_to_screen_pos(pos):
    COORD_FACTOR = 60.5
    x_coord, y_coord = int(pos.real), int(pos.imag)
    screen_pos = (x_coord * COORD_FACTOR, y_coord * COORD_FACTOR)
    return screen_pos


if __name__ == "__main__":
    checkers = Checkers()
    checkers.on_execute()
