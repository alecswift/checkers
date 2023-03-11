import pygame
from sys import exit
from itertools import product

pygame.init()
screen = pygame.display.set_mode((484, 484))
pygame.display.set_caption("Checkers")
clock = pygame.time.Clock()

board_surface = pygame.image.load('graphics/chessboard2.png').convert_alpha()
checkers = pygame.image.load('graphics/checker.png').convert_alpha()


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    for x_coord, y_coord in product(range(0, 364, 121), range(0, 364, 121)):
        screen.blit(board_surface, (x_coord, y_coord))
    screen.blit(checkers, (0, 0), (0, 0, 60, 60)) # black_king
    
    # Draw elements
    # update everything
    # move sprite from one square to another square
    # correlate dictionary of pieces to the display
    pygame.display.update()
    # clock.tick(60) # controls while loop hits/second