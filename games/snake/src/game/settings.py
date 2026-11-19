import pygame
from utils.file_importer import load_images

pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 1920, 1080
CELL_SIZE = 30
ROWS = int(WINDOW_HEIGHT / CELL_SIZE)
COLS = int(WINDOW_WIDTH / CELL_SIZE)
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('snake')

TIMER_FRAMES = load_images("assets", "images", "powerup_timer", scale=6)

SNAKE_COLOR = {
    'default': '#00FF00',
    'multiplier': '#FFD700',
    'bounce': '#AAFF00',
    'ghost': '#7BB274',
    'portal': '#AAFFAA',
    'slow': '#00FF77',
}