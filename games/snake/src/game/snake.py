import pygame
import sys
import random
from game.settings import *
from utils.async_clock import AsyncClock

class Snake():
    def __init__(self):
        self.snake = [(5,5),(5,4),(5,3)]
        self.direction = (0, 1)
        self.clock= AsyncClock(fps=12)
        self.running = True
        self.food = (random.randint(1, ROWS-2), random.randint(1, COLS-2))

    def draw_text(self,text, color, x, y):
        img = FONT.render(text, True, color)
        screen.blit(img, (x, y))


    async def run(self):
        while self.running:
            await self.clock.tick()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w and self.direction != (1, 0):
                        self.direction = (-1, 0)
                    if event.key == pygame.K_s and self.direction != (-1, 0):
                        self.direction = (1, 0)
                    if event.key == pygame.K_a and self.direction != (0, 1):
                        self.direction = (0, -1)
                    if event.key == pygame.K_d and self.direction != (0, -1):
                        self.direction = (0, 1)
            head_row, head_col = self.snake[0]
            d_row, d_col = self.direction
            new_head = (head_row+d_row, head_col+d_col)

            # wall_collision
            if new_head == self.food:
                self.food = (random.randint(1, ROWS-2), random.randint(1, COLS-2))
            else:
                self.snake.pop()
            
            if not (0 <= new_head[0] < ROWS and 0 <= new_head[1] < COLS):
                self.running = False
            # snake_collision
            elif new_head in self.snake:
                self.running = False
            self.snake.insert(0, new_head)

            screen.fill((0,0,0))
            for row, col in self.snake:
                pygame.draw.rect(screen, (0, 255, 0),
                (col*CELL_SIZE, row*CELL_SIZE, CELL_SIZE, CELL_SIZE))
            f_row, f_col = self.food
            pygame.draw.rect(screen, (255, 128, 0), (f_col*CELL_SIZE, f_row*CELL_SIZE, CELL_SIZE, CELL_SIZE))
            score = len(self.snake) - 3
            self.draw_text(f'Score: {score}', (255, 255, 255), 8, 8)
            pygame.display.update()
        
        self.draw_text('WASTED', (128, 0, 0), WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
        self.draw_text(f'Final Score: {score}', (128, 0, 0), WINDOW_WIDTH / 2, 100 + WINDOW_HEIGHT / 2)
        pygame.display.update()
        pygame.time.wait(2000)
        pygame.quit()