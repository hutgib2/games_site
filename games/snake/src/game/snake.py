import pygame
import sys
from random import randint, choice
from game.settings import *
from game.textSprite import TextSprite
from game.notifier import Notifier
from utils.timer import Timer
from utils.async_clock import AsyncClock

# powerup ideas: 
# 1. snake shrinker (done)
# 2. bounce off walls (trails the wall up or down after dying)
# 3. instant turnaround (might not work)
# 4. self.food magnet
# 5. Score multiplier (done)
# 6. bigger orange
# 7. random hole in snake's body

# Steps for adding a feature:
# 1. locate where in the file we need to write new code
# 2. understand how the current code works
# 3. determine how we need to change it
# 4. write in small, testable chunks (testable=can run game and see a change)

class Snake():
    def __init__(self):
        self.score = 0
        self.snake = [(5,5),(5,4),(5,3)]
        self.direction = (0, 1)
        self.food = (randint(1, ROWS-2), randint(1, COLS-2))
        self.running = True
        self.clock= AsyncClock(fps=16)
        
        # powerup
        self.powerup = None
        self.powerup_pos = None
        self.powerup_list = [
            'shrink', 
            'multiplier',
            'bounce'
        ]
        self.powerup_color_map = {
            'shrink': '#FF0000', 
            'multiplier': '#FFFF00',
            'bounce': '#0000FF'
        }
        self.powerup_spawn_timer = Timer(5 * 1000, self.spawn_powerup, repeat=True, autostart=True)
        self.can_bounce = False
        self.powerup_timer = None
        self.score_multiplier = 1
        self.powerup_notifier = Notifier(
            pos=(WINDOW_WIDTH / 1.1, WINDOW_HEIGHT / 24), 
            duration=3000, 
            color='#FFFFFF', 
            size=WINDOW_WIDTH / 24
        )

    def spawn_powerup(self):
        if self.powerup_pos:
            return
        self.powerup = choice(self.powerup_list)
        self.powerup_pos = (randint(1, ROWS-2), randint(1, COLS-2))
        self.powerup_spawn_timer.deactivate()

    def activate_powerup(self):
        self.powerup_notifier.notify(f"{self.powerup.title()}!")
        self.powerup_spawn_timer.activate()

        if self.powerup == 'shrink' and len(self.snake) > 2:
            self.snake.pop()
            self.snake.pop()
        elif self.powerup == 'multiplier':
            self.score_multiplier = 2
        elif self.powerup == 'bounce':
            self.can_bounce = True
        
        self.powerup_timer = Timer(10 * 1000, self.deactivate_powerup, autostart=True)

    # instead of calling a new function in each timer, we can have one deactivate_powerup()
    def deactivate_powerup(self):
        if self.powerup == 'bounce':
            self.can_bounce = False
        elif self.powerup == 'multiplier':
            self.score_multiplier = 1
        self.powerup_timer = None

    # lets do a random direction 
    def bounce(self):
        if self.direction == (-1, 0) or self.direction == (1, 0):
            self.direction = choice([(0, -1), (0, 1)])
        elif self.direction == (0, 1) or self.direction == (0, -1):
            self.direction = choice([(1, 0), (-1, 0)])
        self.move_head()   

    def move_head(self):
        head_row, head_col = self.snake[0]
        d_row, d_col = self.direction
        self.new_head = (head_row+d_row, head_col+d_col)

    def draw_game(self):
        screen.fill((0,0,0))
        for row, col in self.snake:
            pygame.draw.rect(screen, (0, 255, 0),(col*CELL_SIZE, row*CELL_SIZE, CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(screen, (255, 128, 0), (self.food[1]*CELL_SIZE, self.food[0]*CELL_SIZE, CELL_SIZE, CELL_SIZE))
        if self.powerup_pos:
            pygame.draw.rect(screen, self.powerup_color_map[self.powerup], (self.powerup_pos[1]*CELL_SIZE, self.powerup_pos[0]*CELL_SIZE, CELL_SIZE, CELL_SIZE))
            
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
            
            self.move_head()
            if self.new_head == self.food:
                self.food = (randint(1, ROWS-2), randint(1, COLS-2))
                self.score += self.score_multiplier
            else:
                self.snake.pop()
            
            if self.new_head == self.powerup_pos:
                self.activate_powerup()
                self.powerup_pos = None
            
            # wall_collision
            if not (0 <= self.new_head[0] < ROWS and 0 <= self.new_head[1] < COLS):
                self.running = False if not self.can_bounce else self.bounce()

            # snake collision
            elif self.new_head in self.snake:
                self.running = False
            
            self.snake.insert(0, self.new_head)

            self.score_text = TextSprite(f'Score: {self.score}', (WINDOW_WIDTH / 12, WINDOW_HEIGHT / 24), (255, 255, 255), WINDOW_WIDTH / 24, ())
            self.score_text.update()
            self.powerup_spawn_timer.update()
            self.powerup_notifier.update()
            if self.powerup_timer:
                self.powerup_timer.update()
                
            self.draw_game()
            pygame.display.update()
        return self.score