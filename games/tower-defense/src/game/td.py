import math
from game.settings import *

# TODO: reorganise the code into classes
# TODO: add images to game
# TODO: show tower pos before placing
# TODO: redo the map design
# TODO: add different types of enemy with different stats
# TODO: add different types of tower

# Task: creating classes
# class Enemy
# class Tower
# class Bullet ??
# - replace lists with groups for the different sprites

class TowerDefense():
    def __init__(self):
        self.running = True
        self.clock = pygame.time.Clock()
        self.building = True
        self.enemies = []
        # self.enemy_sprites = pygame.group.enemy_sprites
        self.towers = []
        self.bullets = []
        self.spawn_queue = []
        self.cost = 100
        self.spawn_timer = 0
        self.money = 100
        self.lives = 3
        self.current_wave = 0
        self.spawn_delay = 60
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

    def draw_game(self):
        screen.fill((0, 0, 0))
        self.draw_map()
        self.draw_enemies()
        self.draw_tower()
        self.draw_bullets()
        self.draw_display()
        self.draw_build_phase()
        pygame.display.update()

    def draw_map(self):
        for i in range(len(self.way_points)-1):
            pygame.draw.line(screen, (0, 255, 255), self.way_points[i], self.way_points[i+1], 64)

    def spawn_enemy(self):
        return {
            'x': self.way_points[0][0],
            'y': self.way_points[0][1],
            'speed': 1,
            'health': self.current_wave*2,
            'target': 1
        }

    def spawn_tower(self, x, y):
        return {
            'x': x,
            'y': y, 
            'range': WINDOW_WIDTH / 4,
            'damage': 1,
            'cooldown': 0,
            'fire_rate': 16
        }

    def move_enemies(self):
        for enemy in self.enemies[:]:
            if enemy['target'] >= len(self.way_points):
                self.lives -= 1
                self.money += 1
                if self.lives <= 0:
                    self.running = False
                self.enemies.remove(enemy)
                continue
            tx = self.way_points[enemy['target']][0]
            ty = self.way_points[enemy['target']][1]
            dx = tx - enemy['x']
            dy = ty - enemy['y']
            dist = math.hypot(dx, dy)
            if dist < enemy['speed']:
                enemy['target'] += 1
            else:
                enemy['x'] += (dx / dist) * enemy['speed']
                enemy['y'] += (dy / dist) * enemy['speed']

    def draw_enemies(self):
        for enemy in self.enemies[:]:
            pygame.draw.circle(screen, (255, 0, 0), (int(enemy['x']), int(enemy['y'])), 32)

    def draw_tower(self):
        for tower in self.towers[:]:
            pygame.draw.rect(screen, (150, 150, 150), (tower['x']-32, tower['y']-32, 64, 64))
            pygame.draw.circle(screen, (100, 100, 100), (tower['x'], tower['y']), tower['range'], 2)

    def draw_build_phase(self):
        if self.building:
            font = pygame.font.SysFont(None, 128)
            text_pos = (3*WINDOW_WIDTH / 4, WINDOW_HEIGHT / 32)
            pygame.draw.rect(screen, (0, 80, 180), (text_pos[0] - WINDOW_WIDTH / 100, text_pos[1], WINDOW_WIDTH / 4, WINDOW_HEIGHT / 12))
            screen.blit(font.render('start wave', True, (255, 255, 255)), (text_pos[0], text_pos[1]))
            screen.blit(font.render(f'place tower: ${self.cost}', True, (255, 220, 0)), (33*WINDOW_WIDTH / 55, WINDOW_HEIGHT / 8))

    def get_target(self, tower):
        # closest = None
        # closest_dist = tower['range']
        # for enemy in enemies:
        #     dist = math.hypot(enemy['x'] - tower['x'], enemy['y'] - tower['y'])
        #     if dist < closest_dist:
        #         closest = enemy
        #         closest_dist = dist
        # return closest
        furthest = None
        furthest_dist = -1
        for enemy in self.enemies:
            dist = math.hypot(enemy['x'] - tower['x'], enemy['y'] - tower['y'])
            if dist < tower['range']:
                if enemy['target'] > furthest_dist:
                    furthest = enemy
                    furthest_dist = enemy['target']
        return furthest

    def fire(self, tower, target):
        dx = target['x'] - tower['x']
        dy = target['y'] - tower['y']
        dist = math.hypot(dx, dy)
        self.bullets.append({
            'x': tower['x'],
            'y': tower['y'], 
            'dx': dx / dist,
            'dy': dy / dist,
            'speed': 16,
            'damage': tower['damage']   
        })
        tower['cooldown'] = tower['fire_rate']

    def update_bullets(self):
        for bullet in self.bullets[:]:
            bullet['x'] += bullet['dx'] * bullet['speed']
            bullet['y'] += bullet['dy'] * bullet['speed']
            if bullet['x'] < 0 or bullet['x'] > WINDOW_WIDTH or bullet['y'] < 0 or bullet['y'] > WINDOW_HEIGHT:
                self.bullets.remove(bullet)
                continue
            for enemy in self.enemies[:]:
                dist = math.hypot(bullet['x'] - enemy['x'], bullet['y'] - enemy['y'])
                if dist < 32:
                    enemy['health'] -= bullet['damage']
                    if bullet in self.bullets:
                        self.bullets.remove(bullet)
                    if enemy['health'] <= 0:
                        self.enemies.remove(enemy)
                        self.money += 1
                    break

    def update_towers(self):
        for tower in self.towers[:]:
            if tower['cooldown'] > 0:
                tower['cooldown'] -= 1
                continue
            target = self.get_target(tower)
            if target:
                self.fire(tower, target)
            
    def draw_bullets(self):
        for bullet in self.bullets:
            pygame.draw.circle(screen, (255, 220, 0), (int(bullet['x']), int(bullet['y'])), 10)

    def draw_display(self):
        font = pygame.font.SysFont(None, 128)
        screen.blit(font.render(f"money: ${self.money}", True, (255,255,255)), (16, 16))
        screen.blit(font.render(f"current wave: {self.current_wave}", True, (255,255,255)), (16, 256))
        screen.blit(font.render(f"lives: {self.lives}", True, (255,255,255)), (16, 136))

    def start_wave(self, wave_number):
        total = wave_number * 5
        for i in range(total):
            self.spawn_queue.append(self.spawn_enemy())

    def update_spawning(self):
        if not self.spawn_queue:
            return
        self.spawn_timer -= 1

        if self.spawn_timer <= 0:
            self.enemies.append(self.spawn_queue.pop(0))
            self.spawn_timer = self.spawn_delay

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.MOUSEBUTTONDOWN and self.building:
                mx, my = pygame.mouse.get_pos()
                if WINDOW_WIDTH - 750 <= mx <= WINDOW_WIDTH - 250 and 20 <= my <= 120:
                    self.building = False
                    self.wave_complete = False
                    self.start_wave(self.current_wave)
                elif self.money >= self.cost:
                    self.towers.append(self.spawn_tower(mx, my))
                    self.money -= self.cost
                    self.cost += 10

    def run(self):
        while self.running:
            self.handle_events()         
            self.move_enemies()
            self.update_towers()
            self.update_bullets()
            self.update_spawning()
            if not self.spawn_queue and not self.enemies and not self.wave_complete:
                self.current_wave += 1
                self.wave_complete = True
                self.building = True
            
            self.draw_game()