from game.settings import *

class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, direction, speed, damage, groups):
        super().__init__(groups)
        self.pos = pos
        self.direction = direction
        self.speed = speed
        self.damage = damage
        self.color = (255, 200, 0)
        self.radius = 10

    def update(self):
        pygame.draw.circle(screen, self.color, (int(self.pos[0]), int(self.pos[1])), self.radius)