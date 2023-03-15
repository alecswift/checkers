# to do
# game logic
#   improve readability of mouse button up method
#   add tests: atleast 10
# formatting
#   doc strings
#   type hinting for function calls
#   readme

from itertools import product
import pygame
from time import sleep
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
        # create valid paths is on_loop method for current player? possibly to much work
        # every loop so maybe no
        if self._current_checker is None:
            return
        # add player variable for # 2 player
        if self._capture_path is not None:
            # change to retrieving paths: could be mutiple possible future capture paths?
            paths = []
            piece = self._board.board[self._capture_path]
            self._curr_player.next_move((self._capture_path,), paths, piece, False)
            valid_paths = self._curr_player.prune_paths(paths)
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

            # middle of end path square
            screen_target = convert_to_screen_pos(end_pos, 30.25)
            pos_selected = self._current_checker.rect.collidepoint(screen_target)
            if not is_capture_move and pos_selected:
                self._curr_player.no_capture_move(start_pos, end_pos)
                self._current_checker.pos = end_pos
                self.switch_player()
            if is_capture_move and pos_selected:
                new_path = self._curr_player.capture_move(path, self._next_player)
                self._current_checker.pos = end_pos
                self._board_image.remove_checker(opp_pos)
                capture_remaining = 2 < len(new_path)
                if capture_remaining:
                    self._capture_path = end_pos
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
        paths = self._curr_player.potential_paths()
        if not paths:
            sleep(2)
            color = self._next_player.color
            win_surface = pygame.image.load(f"graphics/{color}win.png").convert_alpha()
            self._screen.blit(win_surface, (0, 0))
            pygame.display.update()
            sleep(5)
            self._running = False

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
        for x_coord, y_coord in product(range(0, 364, 121), range(0, 361, 120)):
            screen.blit(self._surface, (x_coord, y_coord))

    def remove_checker(self, pos):
        for checker in self._checkers:
            if checker.pos == pos:
                checker.kill()
                return


class CheckerSprite(pygame.sprite.Sprite):
    def __init__(self, pos, color):
        super().__init__()
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
        promotion_row = 0 if self._color == "black" else 7
        curr_row = self._pos.imag
        if curr_row == promotion_row:
            self.promote()

    @property
    def color(self):
        return self._color

    # https://stackoverflow.com/questions/16825645/how-to-make-a-sprite-follow-your-mouse-cursor-using-pygame
    def update(self):
        """Change the position of the checker based on the piece position data member"""
        self.rect.topleft = convert_to_screen_pos(self._pos)

    def update_from_mouse(self):
        "move the checker based on the mouse position"
        # board.board[self._piece.pos] = "empty" # change so it only does this once or impossible?
        # add layering over other checkers
        pos = pygame.mouse.get_pos()
        self.rect.center = pos

    def promote(self):
        image_path = image_path = f"graphics/{self._color}_king.png"
        self.image = pygame.image.load(image_path)


def convert_to_screen_pos(pos, adder=0):
    COORD_FACTOR = 60.5
    x_coord, y_coord = int(pos.real), int(pos.imag)
    screen_pos = (x_coord * COORD_FACTOR + adder, y_coord * COORD_FACTOR + adder)
    return screen_pos


if __name__ == "__main__":
    checkers = Checkers()
    checkers.on_execute()
