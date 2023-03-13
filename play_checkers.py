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

import pygame
from sys import exit
from board import BoardImage
from player import Player


class Checkers:
    def __init__(self):
        self._running = True
        self._screen = None
        self._size = self.weight, self.height = 484, 484
        self._caption = None
        self._board_image = None
        self._player_1 = None
        self._player_2 = None
        self._curr_player = None
        self._current_checker = None

    def on_init(self):
        pygame.init()
        self._screen = pygame.display.set_mode(self._size)
        self._caption = pygame.display.set_caption("Checkers")

        board_surface = pygame.image.load("graphics/chessboard2.png").convert_alpha()
        checkers = pygame.sprite.Group()
        self._board_image = BoardImage(board_surface, checkers)
        self._player_1 = Player("black", self._board_image)
        self._player_2 = Player("white", self._board_image)
        self._curr_player = self._player_1
        self._running = True

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
        if event.type == pygame.MOUSEBUTTONUP:
            self.mouse_button_up()

    def mouse_button_up(self) -> None:
        if self._current_checker is None:
            return
        # add player variable for # 2 player
        potential_paths = self._curr_player.potential_paths()
        valid_paths = self._curr_player.prune_paths(potential_paths)
        is_capture_move = len(valid_paths[0]) != 2
        for path in valid_paths:
            if is_capture_move:
                start_pos, _, end_pos, *_ = path
            else:
                start_pos, end_pos = path
            if self._current_checker.piece.pos != start_pos:
                continue
            # could set current paths of piece and iterate through those rather than all paths

            x_coord, y_coord = int(end_pos.real), int(end_pos.imag)
            # middle of end path square
            # function for converting coords from complex to screen coords?
            screen_target = (x_coord * 60.5 + 30.25, y_coord * 60.5 + 30.25)
            pos_selected = self._current_checker.rect.collidepoint(screen_target)
            if not is_capture_move and pos_selected:
                self._curr_player.no_capture_move(path)
                self.switch_player()
            if is_capture_move:
                pass
        self._current_checker.update()
        self._current_checker = None

    def switch_player(self):
        if self._curr_player == self._player_1:
            self._curr_player = self._player_2
        else:
            self._curr_player = self._player_1

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


if __name__ == "__main__":
    checkers = Checkers()
    checkers.on_execute()
