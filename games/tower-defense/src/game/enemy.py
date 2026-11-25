from game.settings import *

# arguments are used to define values that we might want to vary
# OR when the value we want needs to come from the parent class
class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, health, groups):
        super().__init__(groups)
        self.pos = pos
        self.health = health
        self.speed = 1
        self.target = 1
        self.color = (255, 0, 0)
        self.size = 32

    def update(self):
        pygame.draw.circle(screen, self.color, self.pos, self.size)
        # later we will have surfs