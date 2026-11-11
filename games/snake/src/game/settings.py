import pygame

pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 1920, 1080
CELL_SIZE = 30
ROWS = int(WINDOW_HEIGHT / CELL_SIZE)
COLS = int(WINDOW_WIDTH / CELL_SIZE)
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('snake')