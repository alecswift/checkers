import pygame
from sys import exit
from itertools import product
from checkers import Board, Player, Piece

pygame.init()
screen = pygame.display.set_mode((484, 484))
pygame.display.set_caption("Checkers")
clock = pygame.time.Clock()

board = Board()
player_1 = Player("black", board)
player_2 = Player("white", board)


class BoardImage(Board):
    def __init__(self, surface, checkers):
        super().__init__()
        self._screen = pygame.display.set_mode((484, 484))
        self._checkers = checkers  # group of checkers sprites
        self._surface = surface

    def display_board(self, screen):
        for x_coord, y_coord in product(range(0, 364, 121), range(0, 364, 121)):
            screen.blit(board_surface, (x_coord, y_coord))

    def set_checkers(self):
        for piece in self.board.values():
            if piece in (None, "empty"):
                continue
            else:
                checkers.add(CheckerSprite(piece))


class CheckerSprite(pygame.sprite.Sprite):
    """moves a clenched fist on the screen, following the mouse"""

    # factor to multiply x and y of the piece, so it is displayed properly on the screen
    COORD_FACTOR = 60.5

    def __init__(self, piece):
        super().__init__()
        self._piece = piece
        image_path = f"graphics/{piece.color}_piece.png"
        self.image = pygame.image.load(image_path).convert_alpha()
        x_coord, y_coord = int(piece.pos.real), int(piece.pos.imag)
        screen_pos = (x_coord * self.COORD_FACTOR, y_coord * self.COORD_FACTOR)
        self.rect = self.image.get_rect(topleft=(screen_pos))

    # https://stackoverflow.com/questions/16825645/how-to-make-a-sprite-follow-your-mouse-cursor-using-pygame
    def update(self):
        "move the checker based on the mouse position"
        # board.board[self._piece.pos] = "empty" # change so it only does this once or impossible?
        # add layering over other checkers
        pos = pygame.mouse.get_pos()
        self.rect.center = pos


board_surface = pygame.image.load("graphics/chessboard2.png").convert_alpha()
checkers = pygame.sprite.Group()
board_image = BoardImage(board_surface, checkers)
board_image.set_checkers()  # set outside loop for initial state
current_checker = None
# correlate piece position tuples with piece position multiply x and y by 60.5
# 6,5 -> 6*60.5, 5*60.5

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONUP:
            current_checker = None
            # go back to initial position

    # Draw elements
    # screen.blit(checkers, (0,0), (0, 60, 60, 60)) # black man
    # screen.blit(checkers, (6*60.5, 5*60.5), (0, 0, 60, 60)) # black king
    # screen.blit(checkers, (60.5,60.5), (60, 60, 60, 60)) # white man
    # screen.blit(checkers, (60.5,0), (60, 0, 60, 60)) # white king
    # set this state outside of game loop, save the state and used the saved
    # state rather than the board class everytime until a move has happened
    # at which point update the state
    board_image.display_board(screen)
    checkers.draw(screen)

    # User input
    mouse_pos = pygame.mouse.get_pos()
    if current_checker is not None:
        mouse_pressed, *_ = pygame.mouse.get_pressed()
        if current_checker.rect.collidepoint(mouse_pos) and mouse_pressed:
            current_checker.update()
    else:
        for checker in checkers:
            mouse_pressed, *_ = pygame.mouse.get_pressed()
            if checker.rect.collidepoint(mouse_pos) and mouse_pressed:
                checker.update()
                current_checker = checker

    # possibly rect collisions for landing on specific squares?
    # pygame.mouse position collides with a players piece plus press to pick up piece

    # update everything
    # move sprite from one square to another square
    # correlate dictionary of pieces to the display
    pygame.display.update()
    # clock.tick(60) # controls while loop hits/second

if __name__ == "__main__":
    main()
