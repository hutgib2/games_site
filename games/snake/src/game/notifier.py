from game.settings import *
from game.textSprite import TextSprite
# from utils.timer import Timer

class Notifier():
    def __init__(self, pos, duration, color, size=128):
        self.pos = pos
        self.duration = duration
        self.color = color
        self.size  = size
        self.start_time = 0
        self.notification = None

    def notify(self, text):
        self.notification = TextSprite(text, self.pos, self.color, self.size, ())
        self.start_time = pygame.time.get_ticks()

    def update(self):
        if self.notification:
            self.notification.update()
            if pygame.time.get_ticks() - self.start_time >= self.duration:
                self.notification = None
                self.start_time = 0