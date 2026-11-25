from game.settings import *

class Tower(pygame.sprite.Sprite):
    def __init__(self, pos, range, damage, cooldown, fire_rate, groups):
        super().__init__(groups)
        self.pos = pos
        self.range = range
        self.damage = damage
        self.cooldown = cooldown
        self.fire_rate = fire_rate

    def update(self):
        pygame.draw.rect(screen, (150, 150, 150), (self.pos[0]-32, self.pos[1]-32, 64, 64))
        pygame.draw.circle(screen, (100, 100, 100), (self.pos[0], self.pos[1]), self.range, 2)