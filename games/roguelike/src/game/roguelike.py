#Import packages
import pygame
import sys
import random
import math
import asyncio
from game.settings import *
from game.textSprite import TextSprite
from utils.async_clock import AsyncClock
from utils.timer import Timer

WEB = sys.platform == "emscripten"

# TODO: hook up high score to database
# TODO: look into failed melee collision on left side of player

class Roguelike():
    def __init__(self):
        self.running = True
        self.clock = AsyncClock(fps=150) if WEB else AsyncClock(60)
        self.score = 0
        self.powerups = []
        self.active_effects = {}
        self.particles = []
        self.highscore = self.load_high_score()
        
        self.powerup_color_map = {
            'speed boost': (80, 255, 80), 
            'nuke': (255, 0, 255),
            'long reach': (150, 75, 0),
            'rear shot': (255, 165, 0),
            'side shot': (100, 0, 100),
            'shotgun': (255, 192, 203),
            'faster swing': (128, 128, 128)
        }

        # melee
        self.angle = 0
        self.rotation_speed = 0.1
        self.radius = 200

        # player
        self.player_health = 3
        self.player_x = WINDOW_WIDTH // 2
        self.player_y = WINDOW_HEIGHT // 2
        self.player_speed = 8
        self.direction = (0, -1)
        self.dx = 1
        self.dy = 0
        
        # bullets
        self.bullets = []
        self.bullet_speed = 32
        self.can_shoot = False
        self.shoot_timer = Timer(200, self.reload, repeat=True, autostart=True)
        
        # demons
        self.enemies = []
        self.current_wave = 1
        self.invincible_timer = 0
        self.last_idle_direction = (0,0)
        self.enemies.append(self.spawn_enemy())
    
    def get_spawn_pos(self):
        side = random.choice(['left', 'right', 'top', 'bottom'])
        if side == 'top':
            x, y = random.randint(0, WINDOW_WIDTH), 0
        elif side == 'bottom':
            x, y = random.randint(0, WINDOW_WIDTH), WINDOW_HEIGHT
        elif side == 'left':
            x, y = 0, random.randint(0, WINDOW_HEIGHT)
        elif side == 'right':
            x, y = WINDOW_WIDTH, random.randint(0, WINDOW_HEIGHT)
        return x, y

    def spawn_enemy(self):
        x, y = self.get_spawn_pos()
        return {'x': x, 'y': y, 'speed': 4, 'health': 1, 'type': 'minion', 'size': 64}

    def spawn_boss(self):
        x, y = self.get_spawn_pos()
        return {'x': x, 'y': y, 'speed': 2, 'health': self.current_wave, 'type': 'boss', 'size': 256}

    def spawn_mob(self):
        x, y = self.get_spawn_pos()
        return {'x': x, 'y': y, 'speed': 10, 'health': 1, 'type': 'mob', 'size': 32}

    def spawn_powerup(self, enemy):
        ptype = random.choices(['speed boost', 'nuke', 'long reach', 'rear shot', 'side shot', 'shotgun', 'faster swing'], weights = [20, 20, 20, 20, 20, 20, 20])[0]
        return {'type': ptype, 'x': enemy['x'], 'y': enemy['y'], 'timer': 1000}

    def apply_powerup(self, ptype):
        if ptype == 'speed boost':
            self.player_speed = 16
        elif ptype == 'nuke':
            self.score += len(self.enemies)
            self.enemies = []
            self.next_wave()
        elif ptype == 'long reach':
            self.radius = 600       
        
        if ptype != 'nuke':
            self.active_effects[ptype] = 300

    def remove_powerup(self, ptype):
        if ptype == 'speed boost':
            self.player_speed = 8
        if ptype == 'long reach':
            self.radius = 200

    def choose_direction(self):
        directions = [[0, 1], [1, 0], [0, -1], [-1, 0], [1, 1], [-1, -1], [1, -1], [-1, 1]]
        while self.direction == [0, 0] or self.direction == self.last_idle_direction:
            self.direction = random.choice(directions)
        self.last_idle_direction = self.direction

    def kill_enemy(self, enemy):
        self.score += 1
        for _ in range(6):
            a = random.uniform(0, 2*math.pi)
            speed = random.uniform(1, 5)
            self.particles.append({'x': enemy['x']+enemy['size'] // 2, 'y': enemy['y']+enemy['size'] // 2, 'dx': math.cos(a)*speed, 'dy': math.sin(a)*speed, 'life': 20, 'color': (255, random.randint(50, 150), 0)})
        if random.random() <= 0.02:
            self.powerups.append(self.spawn_powerup(enemy))
        self.enemies.remove(enemy)

    def next_wave(self):
        self.current_wave += 1
        self.player_x = WINDOW_WIDTH // 2
        self.player_y = WINDOW_HEIGHT // 2
        self.bullets = []
        if self.player_health < 3:
            self.player_health += 1
        for i in range(self.current_wave):
            self.enemies.append(self.spawn_enemy())
            if i == 0 and self.current_wave % 5 == 0:
                self.enemies.append(self.spawn_boss())
            if (i + 1) % 3 == 0 and self.current_wave %3 == 0:
                self.enemies.append(self.spawn_mob())

    def colliding(self, ax, ay, asize, bx, by, bsize):
        center_ax = ax+asize // 2
        center_ay = ay+asize // 2
        center_bx  = bx+bsize // 2
        center_by = by+bsize // 2
        if abs(center_ax-center_bx) <= (asize+bsize) // 2 and abs(center_ay-center_by) <= (asize+bsize) // 2:
            return True
        else:
            return False

    def load_high_score(self):
        try:
            with open("assets/highscore.txt", "r") as file:
                return int(file.read())
        except FileNotFoundError:
            return 0

    def save_high_score(new_score):
        with open("assets/highscore.txt", "w") as file:
            file.write(str(new_score))

    def reload(self):
        self.can_shoot = True

    def shoot(self):
        self.direction = [self.dx, self.dy]
        if self.direction == [0,0]:
            self.choose_direction()
        if 'rear shot' in self.active_effects:
            self.bullets.append([self.player_x, self.player_y, -self.direction[0], -self.direction[1]])
        if 'side shot' in self.active_effects:
            self.bullets.append([self.player_x, self.player_y, self.direction[1], self.direction[0]])
            self.bullets.append([self.player_x, self.player_y, -self.direction[1], -self.direction[0]])
        if 'shotgun' in self.active_effects:
            for sign in [-1, 1]:
                self.offset = sign*math.radians(30)
                new_dx = self.dx*math.cos(self.offset) - self.dy*math.sin(self.offset)
                new_dy = self.dx*math.sin(self.offset) + self.dy*math.cos(self.offset)
                self.bullets.append([self.player_x, self.player_y, new_dx, new_dy])
        self.bullets.append([self.player_x, self.player_y, self.direction[0], self.direction[1]])
        self.can_shoot = False

    def draw_game(self):
        screen.fill((0,0,0))

        # HEALTH BAR
        pygame.draw.rect(screen, (255, 0, 0), (16, 100, 600, 40))
        pygame.draw.rect(screen, (0, 255, 0), (16, 100, int(600*(self.player_health / 3)), 40))

        # PLAYER
        if self.invincible_timer == 0 or self.invincible_timer % 10 < 5:
            pygame.draw.rect(screen, (0, 255, 0),  (self.player_x, self.player_y, 64, 64))
            pygame.draw.line(screen, (255, 255, 0), (self.player_x+32, self.player_y+32), (self.tip_x, self.tip_y), 16)

        # ENEMIES
        for enemy in self.enemies:
            if enemy['type'] == 'minion':
                width = 64
                color = (255, 0, 0)
            elif enemy['type'] == 'mob':
                width = 32
                color = (0, 255, 255)
            else:
                width = 64 + 192*(enemy['health']/self.current_wave)
                color = (200, 0, 200)
            
            pygame.draw.rect(screen, color, (enemy['x'], enemy['y'], width, width))


        # BULLETS
        for bullet in self.bullets:
            pygame.draw.rect(screen, (255, 255, 255), (bullet[0], bullet[1], 32, 32))

        # POWERUPS
        for powerup in self.powerups:
            pygame.draw.circle(screen, self.powerup_color_map[powerup['type']], (powerup['x'], powerup['y']), 20)
        
        for particle in self.particles:
            size = max(1, particle['life'] // 4)
            pygame.draw.rect(screen, particle['color'], (int(particle['x']), int(particle['y']), size, size))
        
        # SCORES
        screen.blit(FONT.render(f"score: {self.score}", True, (255,255,255)), (16, 16))
        screen.blit(FONT.render(f"current wave: {self.current_wave}", True, (255,255,255)), (512, 16))
        screen.blit(FONT.render(f"high score: {max(self.highscore,self.score)}", True, (255,255,255)), (1280, 16))
        pygame.display.update()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN and (event.key == pygame.K_g or event.key == pygame.K_h):
                self.rotation_speed *= -1
                
        keys = pygame.key.get_pressed()
        self.dx = self.dy = 0
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.player_x -= self.player_speed
            self.dx = -1
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.player_x += self.player_speed
            self.dx = 1
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.player_y += self.player_speed
            self.dy = 1
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.player_y -= self.player_speed
            self.dy = -1
        if (keys[pygame.K_l] or keys[pygame.K_SPACE] or keys[pygame.K_RETURN] or keys[pygame.K_z]) and self.can_shoot:
            self.shoot()

    async def run(self):
        while self.running:
            await self.clock.tick()
            self.handle_events()

            if self.invincible_timer > 0:
                self.invincible_timer -= 1
            
            # melee weapon
            if 'faster swing' in self.active_effects:
                self.angle += self.rotation_speed * 4
            else:
                self.angle += self.rotation_speed
            self.tip_x = self.player_x + 32 + self.radius * math.cos(self.angle)
            self.tip_y = self.player_y + 32 + self.radius * math.sin(self.angle)
            
            self.player_x =  max(0, min(self.player_x, WINDOW_WIDTH - 64))
            self.player_y = max(0, min(self.player_y, WINDOW_HEIGHT - 64))

            self.shoot_timer.update()
                
        # MOVE ENEMIES
            for enemy in self.enemies:
                if enemy['x'] < self.player_x:
                    enemy['x'] += enemy['speed']
                elif enemy['x'] > self.player_x:
                    enemy['x'] -= enemy['speed']
                if enemy['y'] < self.player_y:
                    enemy['y'] += enemy['speed']
                elif enemy['y'] > self.player_y:
                    enemy['y'] -= enemy['speed']

        # PARTICLES
            for particle in self.particles[:]:
                particle['x'] += particle['dx']
                particle['y'] += particle['dy']
                particle['life'] -= 1
                if particle['life'] <= 0:
                    self.particles.remove(particle)

        # POWERUPS
            for powerup in self.powerups[:]:
                powerup['timer'] -= 1
                if powerup['timer'] == 0:
                    self.powerups.remove(powerup)
                    continue
                if self.colliding(self.player_x, self.player_y, 64, powerup['x'], powerup['y'], 32):
                    self.apply_powerup(powerup['type'])
                    self.powerups.remove(powerup)

            for effect in list(self.active_effects.keys()):
                self.active_effects[effect] -= 1
                if self.active_effects[effect] <= 0:
                    self.remove_powerup(effect)
                    del self.active_effects[effect]
                    
        # MOVE BULLETS
            for bullet in self.bullets[:]:
                bullet[0] -= bullet[2]*self.bullet_speed
                bullet[1] -= bullet[3]*self.bullet_speed

                if bullet[0] < 0 or bullet[0] > WINDOW_WIDTH or bullet[1] < 0 or bullet[1] > WINDOW_HEIGHT:
                    if bullet in self.bullets:
                        self.bullets.remove(bullet)
                    continue
        
        # COLLISIONS
            # ENEMY AND BULLET            
                for enemy in self.enemies[:]:
                    if self.colliding(bullet[0], bullet[1], 32, enemy['x'], enemy['y'], enemy['size']):
                        try:
                            self.bullets.remove(bullet)
                        except ValueError:
                            continue
                        enemy['health'] -= 1
                        if enemy['health'] == 0:
                            self.kill_enemy(enemy)
                        if len(self.enemies) ==  0:
                            self.next_wave()
                        break

            # ENEMY AND SWORD                    
            for enemy in self.enemies[:]:
                self.dif_x = enemy['x'] - (self.player_x + 32)
                self.dif_y = enemy['y'] - (self.player_y + 32)
                distance = math.hypot(self.dif_x, self.dif_y)
                dif_angle = abs(math.atan2(self.dif_y, self.dif_x) - self.angle)  % (2 * math.pi)
                if (distance <= self.radius) and (dif_angle <= math.radians(30)) and enemy['type'] != 'boss':
                    enemy['health'] -= 1
                    if enemy['health'] == 0:
                        self.kill_enemy(enemy)
                    if len(self.enemies) ==  0:
                        self.next_wave()
                    break

            # ENEMY AND PLAYER
            for enemy in self.enemies[:]:
                if self.colliding(self.player_x, self.player_y, 64, enemy['x'], enemy['y'], enemy['size']) and self.invincible_timer == 0:
                    self.player_health -= 1
                    self.invincible_timer = 60
                    if self.player_health <= 0:
                        self.running = False
            
            self.draw_game()
        return self.score