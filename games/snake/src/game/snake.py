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
# 2. bounce off walls (done)
# 3. Score multiplier (done)
# 4. bigger orange (done)
# 5. pass through body (done)
# 6. slower snake (done)
# 7. portal (done)

# Steps for adding a feature:
# 1. locate where in the file we need to write new code
# 2. understand how the current code works
# 3. determine how we need to change it
# 4. write in small, testable chunks (testable=can run game and see a change)


# TASK: shrink update
# we are shrinking the snake to len 3 when active
# after we want him to grow on each frame until he gets to the previous length
# think, how do we know what the previous length was?
# how can we make him grow ?


class Snake():
    def __init__(self):
        self.score = 0
        self.snake = [(5,5),(5,4),(5,3)]
        self.old_snake_length = len(self.snake)
        self.snake_color = SNAKE_COLOR['default']
        self.direction = (0, 1)
        self.running = True
        self.clock = AsyncClock(fps=15)
        
        # powerup
        self.powerup = None
        self.powerup_pos = None
        self.powerup_list = [
            'shrink', 
            'multiplier',
            'bounce',
            'grow',
            'ghost',
            'slow',
            'portal',
        ]
        self.powerup_color_map = {
            'shrink': '#FF0000', 
            'multiplier': '#FFFF00',
            'bounce': '#0000FF',
            'grow': '#FF00FF',
            'ghost': '#FFFFFF',
            'slow': '#00FFFF',
            'portal': '#770077'
        }
        self.powerup_spawn_timer = Timer(15 * 1000, self.spawn_powerup, repeat=True, autostart=True)
        self.is_shrunk = False
        self.can_bounce = False
        self.powerup_timer = None
        self.grow_food = False
        self.is_ghost = False
        self.score_multiplier = 1
        self.can_teleport = False
        self.powerup_notifier = Notifier(
            pos=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 24), 
            duration=3000, 
            color='#FFFFFF',
            size=WINDOW_WIDTH / 24
        )
        self.spawn_food()

    def increase_food_size(self):
        row, col = self.food[0]
        self.food.append([row+1, col])
        self.food.append([row, col+1])
        self.food.append([row+1, col+1])
        self.food.append([row-1, col])
        self.food.append([row, col-1])
        self.food.append([row-1, col-1])
        self.food.append([row+1, col-1])
        self.food.append([row-1, col+1])


    def spawn_food(self):
        self.food = [self.rand_coord()]
        while self.food in self.snake or self.food[0][0] == self.snake[0][0] or self.food[0][1] == self.snake[0][1]:
            self.food = [self.rand_coord()]
        
        if self.grow_food == True:
            self.increase_food_size()

    def rand_coord(self):
        return [randint(1, ROWS-2), randint(1, COLS-2)]

    def spawn_powerup(self):
        if self.powerup_pos:
            return
        self.powerup = choice(self.powerup_list)
        self.powerup_pos = self.rand_coord()
        self.powerup_spawn_timer.deactivate()

    # replace the if elif chains with match case
    def activate_powerup(self):
        self.powerup_notifier.notify(f"{self.powerup.title()}!")
        self.powerup_spawn_timer.activate()
        
        match self.powerup:
            case 'shrink':
                self.old_snake_length = len(self.snake)
                while len(self.snake) > 3:
                    self.snake.pop()
            case 'multiplier':
                self.score_multiplier = 2
            case 'bounce':
                self.can_bounce = True
            case 'grow':
                self.grow_food = True
                self.increase_food_size()
            case 'ghost':
                self.is_ghost = True
            case 'slow':
                self.clock = AsyncClock(fps=5)
            case 'portal':
                self.can_teleport = True

        if self.powerup in ['ghost', 'bounce', 'slow', 'portal']:
            self.snake_color = SNAKE_COLOR[self.powerup]

        self.powerup_timer = Timer(10 * 1000, self.deactivate_powerup, autostart=True)

    def deactivate_powerup(self):
        match self.powerup:
            case 'shrink':
                self.is_shrunk = True
            case 'multiplier':
                self.score_multiplier = 1
            case 'bounce':
                self.can_bounce = False
            case 'grow':
                self.grow_food = False
                while len(self.food) > 1:
                    self.food.pop()           
            case 'ghost':
                self.is_ghost = False
            case 'slow':
                self.clock = AsyncClock(fps=15)
            case 'portal':
                self.can_teleport = False
        self.powerup_timer = None
        self.snake_color = SNAKE_COLOR['default']

    def move_head(self):
        head_row, head_col = self.snake[0]
        d_row, d_col = self.direction
        self.new_head = [head_row+d_row, head_col+d_col]

    def bounce(self):
        if self.direction == (-1, 0) or self.direction == (1, 0):
            self.direction = choice([(0, -1), (0, 1)])
        elif self.direction == (0, 1) or self.direction == (0, -1):
            self.direction = choice([(1, 0), (-1, 0)])
        self.move_head()

    def teleport(self):
        if self.direction == (-1, 0):
            self.new_head[0] = ROWS-1
        elif self.direction == (1, 0):
            self.new_head[0] = 1
        elif self.direction == (0, -1):
            self.new_head[1] = COLS-1
        elif self.direction == (0, 1):
            self.new_head[1] = 1

    def draw_game(self):
        screen.fill((0,0,0))
        for row, col in self.snake:
            pygame.draw.rect(screen, self.snake_color,(col*CELL_SIZE, row*CELL_SIZE, CELL_SIZE, CELL_SIZE))
        for row, col in self.food:
            pygame.draw.rect(screen, (255, 128, 0), (col*CELL_SIZE, row*CELL_SIZE, CELL_SIZE, CELL_SIZE))
        if self.powerup_pos:
            pygame.draw.rect(screen, self.powerup_color_map[self.powerup], (self.powerup_pos[1]*CELL_SIZE, self.powerup_pos[0]*CELL_SIZE, CELL_SIZE, CELL_SIZE))
        if self.powerup_timer:
            progress = self.powerup_timer.get_progress()
            i = int(progress * (len(TIMER_FRAMES) - 1))
            image = TIMER_FRAMES[i]
            timer_progress_rect = image.get_frect(center = (WINDOW_WIDTH - 32, WINDOW_HEIGHT / 10))
            screen.blit(image, timer_progress_rect)
        self.score_text = TextSprite(f'Score: {self.score}', (WINDOW_WIDTH / 12, WINDOW_HEIGHT / 24), ('#FFFFFF'), WINDOW_WIDTH / 24, ())
        self.score_text.update()
        self.powerup_notifier.update()
            
    async def run(self):
        while self.running:
            self.dt = await self.clock.tick() / 1000
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
            if self.new_head in self.food:
                self.spawn_food()
                self.score += self.score_multiplier
                self.old_snake_length += 1
            elif self.is_shrunk and len(self.snake) <= self.old_snake_length:
                if len(self.snake) == self.old_snake_length:
                    self.is_shrunk = False
            else:
                self.snake.pop()
            
            if self.new_head == self.powerup_pos:
                self.activate_powerup()
                self.powerup_pos = None
            
            # wall_collision
            if not (0 <= self.new_head[0] < ROWS and 0 <= self.new_head[1] < COLS):
                if self.can_bounce:
                    self.bounce()
                elif self.can_teleport:
                    self.teleport()
                else:
                    self.running = False

            # snake collision
            elif self.new_head in self.snake and self.is_ghost == False:
                self.running = False
            
            self.snake.insert(0, self.new_head)

            self.powerup_spawn_timer.update()
            if self.powerup_timer:
                self.powerup_timer.update()
                
            self.draw_game()
            pygame.display.update()
        return self.score