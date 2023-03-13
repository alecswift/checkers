import pygame
from sys import exit
from itertools import product
from checkers import Board, Player


class Checkers:
    def __init__(self):
        self._running = True
        self._screen = None
        self._size = self.weight, self.height = 484, 484
        self._caption = None
        self._board_image = None
        self._player_1 = None
        self._player_2 = None
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
        self._running = True

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
        if event.type == pygame.MOUSEBUTTONUP:
            # separate to new function
            if self._current_checker is not None:
                valid_paths = (
                    self._player_1.valid_paths()
                )  # add player variable for # 2 player
                for path in valid_paths:
                    # could set current paths of piece and iterate through those rather than all paths
                    start_pos, end_pos = path
                    screen_target = None
                    if self._current_checker.piece.pos == start_pos:
                        x_coord, y_coord = int(end_pos.real), int(end_pos.imag)
                        screen_target = (
                            x_coord * 60.5 + 30.25,
                            y_coord * 60.5 + 30.25,
                        )  # middle of end path square
                    if (
                        screen_target is not None
                        and self._current_checker.rect.collidepoint(screen_target)
                    ):
                        self._player_1.no_capture_move(path)
                self._current_checker.update()
                self._current_checker = None

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
            if piece in (None, "empty"):
                continue
            else:
                self._checkers.add(CheckerSprite(piece))

    def display_board(self, screen):
        for x_coord, y_coord in product(range(0, 364, 121), range(0, 364, 121)):
            screen.blit(self._surface, (x_coord, y_coord))


class CheckerSprite(pygame.sprite.Sprite):
    """moves a clenched fist on the screen, following the mouse"""

    # factor to multiply x and y of the piece, so it is displayed properly on the screen
    COORD_FACTOR = 60.5

    def __init__(self, piece):
        super().__init__()
        # messy here fix it up
        self._piece = piece
        image_path = f"graphics/{piece.color}_piece.png"
        self.image = pygame.image.load(image_path).convert_alpha()
        # change this to update call elsewhere?
        x_coord, y_coord = int(piece.pos.real), int(piece.pos.imag)
        screen_pos = (x_coord * self.COORD_FACTOR, y_coord * self.COORD_FACTOR)
        self.rect = self.image.get_rect(topleft=(screen_pos))

    @property
    def piece(self):
        return self._piece

    # https://stackoverflow.com/questions/16825645/how-to-make-a-sprite-follow-your-mouse-cursor-using-pygame
    def update(self):
        """Change the position of the checker based on the piece position data member"""
        x_coord, y_coord = int(self._piece.pos.real), int(self._piece.pos.imag)
        self.rect.topleft = (x_coord * self.COORD_FACTOR, y_coord * self.COORD_FACTOR)

    def update_from_mouse(self):
        "move the checker based on the mouse position"
        # board.board[self._piece.pos] = "empty" # change so it only does this once or impossible?
        # add layering over other checkers
        pos = pygame.mouse.get_pos()
        self.rect.center = pos


if __name__ == "__main__":
    checkers = Checkers()
    checkers.on_execute()
