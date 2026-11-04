import pygame
import sys
import random
from game.settings import *
from game.textSprite import TextSprite
from utils.async_clock import AsyncClock

class Snake():
    def __init__(self):
        self.clock= AsyncClock(fps=16)
        self.score = None
        self.menu_sprites = pygame.sprite.Group()
        self.game_over_sprites = pygame.sprite.Group()
        TextSprite('Arcade Snake', (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 3), (128, 0, 0), WINDOW_WIDTH / 16, self.menu_sprites)
        TextSprite('Press enter to play', (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2), (128, 0, 0), WINDOW_WIDTH / 32, (self.menu_sprites, self.game_over_sprites))
        TextSprite('WASTED', (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 3), (128, 0, 0), WINDOW_WIDTH / 16, self.game_over_sprites)
        
    def draw_text(self,text, color, x, y):
        img = FONT.render(text, True, color)
        font_rect = img.get_frect(center=(x, y))
        screen.blit(img, font_rect)


    async def show_menu(self):
        while True:
            await self.clock.tick()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    await self.run()
            
            screen.fill((0,0,0))
            
            if self.score != None:
                self.game_over_sprites.update()
                self.score_text.update()
            else:
                self.menu_sprites.update()

            pygame.display.update()


    async def run(self):
        self.score = 0
        snake = [(5,5),(5,4),(5,3)]
        direction = (0, 1)
        food = (random.randint(1, ROWS-2), random.randint(1, COLS-2))
        running = True
        while running:
            await self.clock.tick()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w and direction != (1, 0):
                        direction = (-1, 0)
                    if event.key == pygame.K_s and direction != (-1, 0):
                        direction = (1, 0)
                    if event.key == pygame.K_a and direction != (0, 1):
                        direction = (0, -1)
                    if event.key == pygame.K_d and direction != (0, -1):
                        direction = (0, 1)
            head_row, head_col = snake[0]
            d_row, d_col = direction
            new_head = (head_row+d_row, head_col+d_col)
        

            # wall_collision
            if new_head == food:
                food = (random.randint(1, ROWS-2), random.randint(1, COLS-2))
            else:
                snake.pop()
            
            if not (0 <= new_head[0] < ROWS and 0 <= new_head[1] < COLS):
                running = False
            # snake collision
            elif new_head in snake:
                running = False
            snake.insert(0, new_head)

            screen.fill((0,0,0))
            for row, col in snake:
                pygame.draw.rect(screen, (0, 255, 0),
                (col*CELL_SIZE, row*CELL_SIZE, CELL_SIZE, CELL_SIZE))
            f_row, f_col = food
            pygame.draw.rect(screen, (255, 128, 0), (f_col*CELL_SIZE, f_row*CELL_SIZE, CELL_SIZE, CELL_SIZE))
            self.score = len(snake) - 3
            self.draw_text(f'Score: {self.score}', (255, 255, 255), WINDOW_WIDTH / 16, WINDOW_HEIGHT / 24)
            pygame.display.update()
        self.score_text = TextSprite(f'Final score: {self.score}', (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 10 + WINDOW_HEIGHT / 2), (128, 0, 0), WINDOW_WIDTH / 32, ())