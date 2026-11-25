from game.settings import *

class Tower(pygame.sprite.Sprite):
    def __init__(self, pos, range, damage, cooldown, fire_rate, groups):
        super().__init__(groups)
        self.pos = pos
        self.range = range
        self.damage = damage
        self.cooldown = cooldown
        self.fire_rate = fire_rate
        self.color = (150, 150, 150)
        self.radius_color = (100, 100, 100)
        self.width = 64

    def update(self):
        pygame.draw.rect(screen, self.color, (self.pos[0]-(self.width / 2), self.pos[1]-(self.width / 2), self.width, self.width))
        pygame.draw.circle(screen, self.radius_color, (self.pos[0], self.pos[1]), self.range, 2)