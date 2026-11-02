import pygame

pygame.init()
FONT = pygame.font.SysFont(None, 64)
CELL_SIZE = 32
ROWS = 32
COLS = 32
WINDOW_WIDTH = COLS * CELL_SIZE
WINDOW_HEIGHT= ROWS * CELL_SIZE
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('snake')