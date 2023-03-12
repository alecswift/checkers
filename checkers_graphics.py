import pygame
from sys import exit
from itertools import product
from checkers import Checkers, Player

pygame.init()
screen = pygame.display.set_mode((484, 484))
pygame.display.set_caption("Checkers")
clock = pygame.time.Clock()

game = Checkers()
player_1 = Player("black", game)
player_2 = Player("white", game)


board_surface = pygame.image.load('graphics/chessboard2.png').convert_alpha()
checkers = pygame.image.load('graphics/checker.png').convert_alpha()
# correlate piece position tuples with piece position multiply x and y by 60.5
# 6,5 -> 6*60.5, 5*60.5

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    # Draw elements
    # screen.blit(checkers, (0,0), (0, 60, 60, 60)) # black man
    # screen.blit(checkers, (6*60.5, 5*60.5), (0, 0, 60, 60)) # black king
    # screen.blit(checkers, (60.5,60.5), (60, 60, 60, 60)) # white man
    # screen.blit(checkers, (60.5,0), (60, 0, 60, 60)) # white king
    for x_coord, y_coord in product(range(0, 364, 121), range(0, 364, 121)):
        screen.blit(board_surface, (x_coord, y_coord))
    for pos, val in game.board.items():
        if val in (None, 'empty'):
            continue
        if val.color == 'black':
            screen.blit(checkers, (pos.real * 60.5, pos.imag * 60.5), (0, 60, 60, 60))
        else:
            screen.blit(checkers, (pos.real * 60.5, pos.imag * 60.5), (60, 60, 60, 60))
    # User input
    # possibly rect collisions for landing on specific squares?
    # pygame.mouse position collides with a players piece plus press to pick up piece


    # update everything
    # move sprite from one square to another square
    # correlate dictionary of pieces to the display
    pygame.display.update()
    # clock.tick(60) # controls while loop hits/second