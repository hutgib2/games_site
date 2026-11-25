import math
from game.settings import *
from game.enemy import Enemy
from game.tower import Tower
from game.bullet import Bullet
from utils.timer import Timer
from utils.async_clock import AsyncClock

# HOMEWORK
# choose a theme for the game
# find images for enemies, towers, bg image, map


# TODO: reorganise the code into classes (done)
# TODO: add images to game
# TODO: show tower pos before placing
# TODO: redo the map design
# TODO: add different types of enemy with different stats
# TODO: add different types of tower

class TowerDefense():
    def __init__(self):
        self.running = True
        self.clock = AsyncClock(fps=60)
        self.enemy_sprites = pygame.sprite.Group()
        self.tower_sprites = pygame.sprite.Group()
        self.bullet_sprites = pygame.sprite.Group()
        self.cost = 100
        self.spawn_timer = None
        self.money = 100
        self.lives = 3
        self.current_wave = 0
        self.building = True
        self.wave_complete = False

        self.way_points = [
            (0, WINDOW_HEIGHT / 1.1),
            (WINDOW_WIDTH / 1.1, WINDOW_HEIGHT / 1.1),
            (WINDOW_WIDTH / 1.1, WINDOW_HEIGHT / 1.35),
            (WINDOW_WIDTH / 7, WINDOW_HEIGHT / 1.35),
            (WINDOW_WIDTH / 7, WINDOW_HEIGHT / 2),
            (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2),
            (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 3),
            (WINDOW_WIDTH / 2.5, WINDOW_HEIGHT / 3),
            (WINDOW_WIDTH / 2.5, WINDOW_HEIGHT / 10),
            (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 10),
            (WINDOW_WIDTH / 2, 0)
        ]


    def spawn_enemy(self):
        Enemy([self.way_points[0][0], self.way_points[0][1]], self.current_wave*2, self.enemy_sprites)

    def spawn_tower(self, pos):
        Tower(pos, WINDOW_WIDTH / 4, 1, 0, 16, self.tower_sprites)
        
    def move_enemies(self):
        # replace the indexing into a dict, with accessing the class attributes
        for enemy in self.enemy_sprites:
            if enemy.target >= len(self.way_points):
                self.lives -= 1
                self.money += 1
                if self.lives <= 0:
                    self.running = False
                enemy.kill()
                continue
            tx = self.way_points[enemy.target][0]
            ty = self.way_points[enemy.target][1]
            dx = tx - enemy.pos[0]
            dy = ty - enemy.pos[1]
            dist = math.hypot(dx, dy)
            if dist < enemy.speed:
                enemy.target += 1
            else:
                enemy.pos[0] += (dx / dist) * enemy.speed
                enemy.pos[1] += (dy / dist) * enemy.speed

    def draw_build_phase(self):
        if self.building:
            font = pygame.font.SysFont(None, 128)
            text_pos = (3*WINDOW_WIDTH / 4, WINDOW_HEIGHT / 32)
            pygame.draw.rect(screen, (0, 80, 180), (text_pos[0] - WINDOW_WIDTH / 100, text_pos[1], WINDOW_WIDTH / 4, WINDOW_HEIGHT / 12))
            screen.blit(font.render('start wave', True, (255, 255, 255)), (text_pos[0], text_pos[1]))
            screen.blit(font.render(f'place tower: ${self.cost}', True, (255, 220, 0)), (33*WINDOW_WIDTH / 55, WINDOW_HEIGHT / 8))

    def get_target(self, tower):
        furthest = None
        furthest_dist = -1
        for enemy in self.enemy_sprites:
            dist = math.hypot(enemy.pos[0] - tower.pos[0], enemy.pos[1] - tower.pos[1])
            if dist < tower.range:
                if enemy.target > furthest_dist:
                    furthest = enemy
                    furthest_dist = enemy.target
        return furthest

    def fire(self, tower, target):
        dx = target.pos[0] - tower.pos[0]
        dy = target.pos[1] - tower.pos[1]
        dist = math.hypot(dx, dy)
        Bullet([tower.pos[0], tower.pos[1]], [dx / dist, dy / dist], 16, tower.damage, self.bullet_sprites)
        tower.cooldown = tower.fire_rate

    def update_bullets(self):
        for bullet in self.bullet_sprites:
            bullet.pos[0] += bullet.direction[0] * bullet.speed
            bullet.pos[1] += bullet.direction[1] * bullet.speed
            if bullet.pos[0] < 0 or bullet.pos[0] > WINDOW_WIDTH or bullet.pos[1] < 0 or bullet.pos[1] > WINDOW_HEIGHT:
                bullet.kill()
                continue
            for enemy in self.enemy_sprites:
                dist = math.hypot(bullet.pos[0] - enemy.pos[0], bullet.pos[1] - enemy.pos[1])
                if dist < 32:
                    enemy.health -= bullet.damage
                    if bullet in self.bullet_sprites:
                        bullet.kill()
                    if enemy.health <= 0:
                        enemy.kill()
                        self.money += 1
                    break

    def update_towers(self):
        for tower in self.tower_sprites:
            if tower.cooldown > 0:
                tower.cooldown -= 1
                continue
            target = self.get_target(tower)
            if target:
                self.fire(tower, target)
            
    def draw_bullets(self):
        for bullet in self.bullet_sprites:
            pygame.draw.circle(screen, (255, 220, 0), (int(bullet.pos[0]), int(bullet.pos[1])), 10)

    def draw_display(self):
        font = pygame.font.SysFont(None, 128)
        screen.blit(font.render(f"money: ${self.money}", True, (255,255,255)), (16, 16))
        screen.blit(font.render(f"current wave: {self.current_wave}", True, (255,255,255)), (16, 256))
        screen.blit(font.render(f"lives: {self.lives}", True, (255,255,255)), (16, 136))

    def draw_game(self):
        screen.fill((0, 0, 0))
        self.draw_map()
        self.enemy_sprites.update()
        self.tower_sprites.update()
        self.draw_bullets()
        self.draw_display()
        self.draw_build_phase()
        pygame.display.update()

    def draw_map(self):
        for i in range(len(self.way_points)-1):
            pygame.draw.line(screen, (0, 255, 255), self.way_points[i], self.way_points[i+1], 64)

    def start_wave(self):
        self.spawn_timer = Timer(250, self.spawn_enemy, repeat=self.current_wave * 5, autostart=True)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.MOUSEBUTTONDOWN and self.building:
                mx, my = pygame.mouse.get_pos()
                if WINDOW_WIDTH - 750 <= mx <= WINDOW_WIDTH - 250 and 20 <= my <= 120:
                    self.building = False
                    self.wave_complete = False
                    self.start_wave()
                elif self.money >= self.cost:
                    self.spawn_tower([mx, my])
                    self.money -= self.cost
                    self.cost += 10

    def run(self):
        while self.running:
            self.clock.tick()
            self.handle_events()         
            self.move_enemies()
            self.update_towers()
            self.update_bullets()
            if self.spawn_timer:
                self.spawn_timer.update()
            if len(self.enemy_sprites) == 0 and not self.wave_complete:
                self.current_wave += 1
                self.wave_complete = True
                self.building = True
            
            self.draw_game()