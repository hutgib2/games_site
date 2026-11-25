import pygame

class Timer:
    def __init__(self, duration, func = None, repeat = 1, autostart = False):
        self.duration = duration
        self.start_time = 0
        self.active = False
        self.func = func
        self.repeat = repeat
        self.func_exections = 0

        if autostart:
            self.activate()

    def __bool__(self):
        return self.active

    def activate(self):
        self.active = True
        self.start_time = pygame.time.get_ticks()
    
    def deactivate(self):
        self.active = False
        self.start_time = 0
        if self.func_exections < self.repeat or self.repeat==None:
            self.activate()
    
    def stop(self): # Use to temporarily pause a repeating timer
        if self.repeat:
            self.repeat = 0

    def resume(self): # Use to resume a repeating timer
        self.repeat = None # TODO: fix stop and resume for new repeat functionality

    def get_progress(self):
        elapsed_time = pygame.time.get_ticks() - self.start_time
        progress = elapsed_time / self.duration
        return min(progress, 1)

    def update(self):
        if pygame.time.get_ticks() - self.start_time >= self.duration:
            if self.func and self.start_time != 0:
                self.func()
                self.func_exections += 1
            self.deactivate()