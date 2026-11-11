import pygame
import sys
from random import randint, choice
from game.settings import *
from game.textSprite import TextSprite
from utils.timer import Timer
from utils.async_clock import AsyncClock

# powerup ideas: 
# 1. snake shrinker 
# 2. bounce off walls 
# 3. instant turnaround 
# 4. self.food magnet
# 5. Score multiplier maybe? 

# TASK: add powerups to game
# - create a timer that spawns a powerup on the screen
    # just print "powerup" when timer executes

# - start with just snake shrinker and we'll more after
# - when snake eats powerup, activate it

class Snake():
    def __init__(self):
        self.score = 0
        self.snake = [(5,5),(5,4),(5,3)]
        self.direction = (0, 1)
        self.food = (randint(1, ROWS-2), randint(1, COLS-2))
        self.running = True
        self.clock= AsyncClock(fps=16)
        self.powerup_pos = None
        self.powerup_list = ['shrink', 'multiplier']
        self.powerup_spawn_timer = Timer(15 * 1000, self.spawn_powerup, repeat=True, autostart=True)

    def spawn_powerup(self):
        if self.powerup_pos:
            return
        self.powerup_pos = (randint(1, ROWS-2), randint(1, COLS-2))

    def activate_powerup(self):
        self.powerup = choice(self.powerup_list)
        # we need to actually do something with the powerup that is selected
        if self.powerup == 'shrink':
            pass
        
    # def draw_text(self,text, color, x, y):
    #     img = FONT.render(text, True, color)
    #     font_rect = img.get_frect(center=(x, y))
    #     screen.blit(img, font_rect)

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

            if new_head == self.food:
                self.food = (randint(1, ROWS-2), randint(1, COLS-2))
            else:
                self.snake.pop()
                
            if new_head == self.powerup_pos:
                self.activate_powerup()
                self.powerup_pos = None
            
            # wall_collision
            if not (0 <= new_head[0] < ROWS and 0 <= new_head[1] < COLS):
                self.running = False
            # snake collision
            elif new_head in self.snake:
                self.running = False
            self.snake.insert(0, new_head)

            screen.fill((0,0,0))
            for row, col in self.snake:
                pygame.draw.rect(screen, (0, 255, 0),
                (col*CELL_SIZE, row*CELL_SIZE, CELL_SIZE, CELL_SIZE))
            f_row, f_col = self.food
            pygame.draw.rect(screen, (255, 128, 0), (f_col*CELL_SIZE, f_row*CELL_SIZE, CELL_SIZE, CELL_SIZE))
            if self.powerup_pos:
                pygame.draw.rect(screen, (255, 255, 0), (self.powerup_pos[0]*CELL_SIZE, self.powerup_pos[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE))
            
            self.score = len(self.snake) - 3
            self.score_text = TextSprite(f'Score: {self.score}', (WINDOW_WIDTH / 12, WINDOW_HEIGHT / 24), (255, 255, 255), WINDOW_WIDTH / 24, ())
            self.score_text.update()
            self.powerup_spawn_timer.update()
            pygame.display.update()
        return self.score