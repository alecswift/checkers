# to do
# game logic
#   Still max recursion error for random moves can't seem to replicate
#   Add docstrings/typehints
#   Add alpha beta pruning for hard level AI
#   add checker layering
#   add tests: atleast 10
#   refactor calls of cleanup method

from itertools import product
import pygame
from sys import exit, setrecursionlimit
from time import sleep
from typing import Optional
from game import init_state, init_borders, Board, Piece
from checkers_ai import find_ai_move
import game


class Checkers:
    """
    Represents a game of checkers utilizing pygame for UI and a game loop:
    input, update, render
    """

    def __init__(self):
        self._running = True
        self._screen = None
        self._size = 484, 484
        self._caption = None
        self._board_image = None
        self._board = None
        self._player_move = None
        self._ai = True

    def on_init(self):
        """
        Initialize the game and data members including the screen,
        caption, board, board image, player input, and running
        """
        pygame.init()
        self._screen = pygame.display.set_mode(self._size)
        self._caption = pygame.display.set_caption("Checkers")

        board_state = init_state()
        borders = init_borders()
        self._board = Board(board_state, borders)
        board_surface = pygame.image.load("graphics/chessboard2.png").convert_alpha()
        self._board_image = BoardImage(board_surface, pygame.sprite.Group())
        self._board_image.set_checkers(self._board.board_state)

        player_1 = Piece.BLACK
        player_2 = Piece.WHITE
        self._player_move = PlayerMove(player_1, player_2)
        self._running = True

    def on_event(self, event):
        """
        Event actions for checkers quits the user interface if the event type 
        is quit or completes a humans player checker move if the mouse button
        goes up
        """
        if event.type == pygame.QUIT:
            self.on_cleanup()
        if event.type == pygame.MOUSEBUTTONUP:
            self._player_move.mouse_button_up(self._board, self._board_image)
            self.on_render()

    def on_loop(self):
        """
        Make a player move if the player right clicks the mouse of a piece,
        if the current player is AI make an ai move quit the game if a player won
        """
        if self._ai and self._player_move.curr_player == Piece.WHITE:
            self._player_move.make_ai_move(self._board, self._board_image, self._screen)
        else:
            self._player_move.mouse_button_down(self._board_image)
        self.game_won()

    def on_render(self):
        """Render the game board and checker pieces"""
        self._board_image.display_board(self._screen)
        self._board_image.checkers.draw(self._screen)
        pygame.display.update()

    def on_cleanup(self):
        """End the game and quit pygame"""
        pygame.display.quit()
        pygame.quit()
        exit()

    def on_execute(self):
        """Game loop: input, update, render"""
        if self.on_init() == False:
            self._running = False

        while self._running:
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
        self.on_cleanup()

    def game_won(self):
        """
        Returns whether or not a player has won the game based on the number
        of valid paths of the opponent player and quit the game
        """
        paths = self._board.find_valid_moves(self._player_move.curr_player)
        if not paths:
            self.on_render()
            sleep(2)
            color = "black" if self._player_move.next_player == Piece.BLACK else "white"
            win_surface = pygame.image.load(f"graphics/{color}win.png").convert_alpha()
            self._screen.blit(win_surface, (0, 0))
            pygame.display.update()
            sleep(5)
            self.on_cleanup()


class BoardImage:
    """Represents the image of a checkerboard"""

    def __init__(self, surface, checkers):
        self._checkers = checkers  # position: CheckerSprite
        self._surface = surface

    @property
    def checkers(self):
        return self._checkers

    @property
    def surface(self):
        return self._surface

    def set_checkers(self, board):
        """
        Intialize checker sprites from the positions of the given board
        and add them into a sprite group
        """
        for pos, piece in board:
            if piece != Piece.EMPTY:
                self._checkers.add(CheckerSprite(pos, piece))

    def display_board(self, screen):
        """Display the checkerboard onto the screen"""
        for x_coord, y_coord in product(range(0, 364, 121), range(0, 361, 120)):
            screen.blit(self._surface, (x_coord, y_coord))

    def remove_checker(self, pos=None):
        """Remove the CheckerSprite at the given position from the game"""
        if pos is None:
            return
        for checker in self._checkers:
            if checker.pos == pos:
                checker.kill()
                return


class CheckerSprite(pygame.sprite.Sprite):
    """Represents a checker sprite"""

    def __init__(self, pos, piece):
        super().__init__()
        color = "black" if piece == Piece.BLACK else "white"
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
        pos = pygame.mouse.get_pos()
        self.rect.center = pos

    def promote(self):
        """Change the sprite image to a king checker"""
        image_path = image_path = f"graphics/{self._color}_king.png"
        self.image = pygame.image.load(image_path)


class PlayerMove:
    """
    Methods for changing positions of checkers based on player input
    utilizes the current player, next player, current checker, and if there
    was a capture on the last move to make these changes
    """

    def __init__(self, player_1, player_2):
        self._curr_player = player_1
        self._next_player = player_2
        self._current_checker = None
        self._more_captures = None

    @property
    def current_checker(self):
        return self._current_checker

    @current_checker.setter
    def current_checker(self, checker):
        self._current_checker = checker

    @property
    def curr_player(self):
        return self._curr_player

    @property
    def next_player(self):
        return self._next_player

    def mouse_button_down(self, board_image):
        """
        Selects a checker if the player right clicks a checker sprite with
        their mouse and moves it based on the mouse position
        """
        mouse_pos = pygame.mouse.get_pos()
        if self._current_checker is not None:
            mouse_pressed, *_ = pygame.mouse.get_pressed()
            if self._current_checker.rect.collidepoint(mouse_pos) and mouse_pressed:
                self._current_checker.update_from_mouse()
        else:
            for checker in board_image.checkers:
                mouse_pressed, *_ = pygame.mouse.get_pressed()
                if checker.rect.collidepoint(mouse_pos) and mouse_pressed:
                    self._current_checker = checker

    def mouse_button_up(self, state_obj, board_image):
        """
        Places a checker sprite on a new spot if the player selects a valid move.
        Otherwise return the checker sprite to it's original position
        """
        if self._current_checker is None:
            return

        start_pos = self._current_checker.pos
        if self._more_captures is None or self._more_captures == start_pos:
            moves = game.get_moves_from(self.curr_player, start_pos, state_obj)
        else:
            moves = ()

        for move in moves:
            _, positions, skip, captures = move
            _, end_pos = positions
            screen_end_pos = convert_to_screen_pos(end_pos, 30.25)
            pos_selected = self._current_checker.rect.collidepoint(screen_end_pos)
            if pos_selected:
                move = move[:3]
                state_obj.board_state = game.make_move(move, state_obj.board_state)
                self._current_checker.pos = end_pos
                board_image.remove_checker(*skip)
                if 1 < captures:
                    self._more_captures = end_pos
                else:
                    self._more_captures = None
                    self.switch_player()

        self._current_checker.update()
        self._current_checker = None

    def make_ai_move(self, state_obj, board_image, screen):
        """Find the best move based on the board state, then make that
        move and update the game state"""
        move = find_ai_move(state_obj.board_state)
        if not move:
            return

        _, positions, skips = move
        start_pos, *rest = positions
        screen_target = convert_to_screen_pos(start_pos, 30.25)
        for checker in board_image.checkers:
            if checker.rect.collidepoint(screen_target):
                self._current_checker = checker
        for idx, pos in enumerate(rest):
            sleep(1)
            if skips:
                board_image.remove_checker(skips[idx])
            self._current_checker.pos = pos
            self._current_checker.update()
            board_image.display_board(screen)
            board_image.checkers.draw(screen)
            pygame.display.update()

        state_obj.board_state = game.make_move(move, state_obj.board_state)
        self._current_checker = None
        self.switch_player()

    def switch_player(self):
        """
        Represents a change in turn. Switches the current player with the next player
        """
        self._curr_player, self._next_player = self._next_player, self._curr_player


def convert_to_screen_pos(pos, adder = 0):
    """
    Converts a board pos of a checker represented by complex numbers with
    rows and columns 0-7 to a screen position
    """
    COORD_FACTOR = 60.5
    x_coord, y_coord = int(pos.real), int(pos.imag)
    screen_pos = (x_coord * COORD_FACTOR + adder, y_coord * COORD_FACTOR + adder)
    return screen_pos

def convert_to_state_pos(screen_pos):
    """Converts the given screen pos to an internal board state position"""
    COORD_FACTOR = 60.5
    x_coord, y_coord = screen_pos[0] // COORD_FACTOR, screen_pos[1] // COORD_FACTOR
    return complex(x_coord, y_coord)

if __name__ == "__main__":
    setrecursionlimit(2000)
    checkers = Checkers()
    checkers.on_execute()
