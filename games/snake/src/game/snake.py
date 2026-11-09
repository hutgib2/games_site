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
# 4. food magnet
# 5. Score multiplier maybe? 

# TASK: add powerups to game
# - create a timer that spawns a powerup on the screen
    # just print "powerup" when timer executes

# - start with just snake shrinker and we'll more after
# - when snake eats powerup, activate it

class Snake():
    def __init__(self):
        self.clock= AsyncClock(fps=16)
        self.score = None
        self.menu_sprites = pygame.sprite.Group()
        self.game_over_sprites = pygame.sprite.Group()
        self.text_color = (255, 0, 0)
        TextSprite('Special Snake', (WINDOW_WIDTH / 1.5, WINDOW_HEIGHT / 1.8), self.text_color, WINDOW_WIDTH / 12, self.menu_sprites)
        TextSprite('Press enter to play', (WINDOW_WIDTH / 1.5, WINDOW_HEIGHT / 1.25), self.text_color, WINDOW_WIDTH / 24, (self.menu_sprites, self.game_over_sprites))
        TextSprite('Game Over', (WINDOW_WIDTH / 1.5, WINDOW_HEIGHT / 2), self.text_color, WINDOW_WIDTH / 16, self.game_over_sprites)
        self.bg_image = pygame.image.load('assets/images/snake.png')
        self.bg_image = pygame.transform.smoothscale(self.bg_image, (WINDOW_WIDTH, WINDOW_HEIGHT))
        self.powerup_pos = None
        self.powerup_list = ['shrink', 'multiplier']
        self.powerup_spawn_timer = Timer(5 * 1000, self.spawn_powerup, repeat=True, autostart=True)

    def spawn_powerup(self):
        if self.powerup_pos:
            return
        self.powerup_pos = (randint(1, ROWS-2), randint(1, COLS-2))

    def activate_powerup(self):
        self.powerup = choice(self.powerup_list)
        # we need to actually do something with the powerup that is selected
        if self.powerup == 'shrink':
            pass
        
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

            screen.blit(self.bg_image)
            
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
        food = (randint(1, ROWS-2), randint(1, COLS-2))
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
        

            if new_head == food:
                food = (randint(1, ROWS-2), randint(1, COLS-2))
            else:
                snake.pop()
                
            if new_head == self.powerup_pos:
                self.activate_powerup()
                self.powerup_pos = None
            
            # wall_collision
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
            if self.powerup_pos:
                pygame.draw.rect(screen, (255, 255, 0), (self.powerup_pos[0]*CELL_SIZE, self.powerup_pos[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE))
            
            self.score = len(snake) - 3
            self.draw_text(f'Score: {self.score}', (255, 255, 255), WINDOW_WIDTH / 16, WINDOW_HEIGHT / 24)
            self.powerup_spawn_timer.update()
            pygame.display.update()
        self.score_text = TextSprite(f'Final score: {self.score}', (WINDOW_WIDTH / 1.5, WINDOW_HEIGHT / 1.5), self.text_color, WINDOW_WIDTH / 24, ())