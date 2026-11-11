from game.settings import *
from game.snake import Snake
from game.textSprite import TextSprite
import asyncio

class Menu:
    def __init__(self):
        self.bg_image = pygame.image.load('assets/images/snake.png')
        self.bg_image = pygame.transform.smoothscale(self.bg_image, (WINDOW_WIDTH, WINDOW_HEIGHT))
        self.pending_game = None
        self.running = True
        self.menu_sprites = pygame.sprite.Group()
        self.game_over_sprites = pygame.sprite.Group()
        self.text_color = (255, 0, 0)
        self.score = None
        TextSprite('Special Snake', (WINDOW_WIDTH / 1.5, WINDOW_HEIGHT / 1.8), self.text_color, WINDOW_WIDTH / 12, self.menu_sprites)
        TextSprite('Press enter to play', (WINDOW_WIDTH / 1.5, WINDOW_HEIGHT / 1.25), self.text_color, WINDOW_WIDTH / 24, (self.menu_sprites, self.game_over_sprites))
        TextSprite('Game Over', (WINDOW_WIDTH / 1.5, WINDOW_HEIGHT / 2), self.text_color, WINDOW_WIDTH / 16, self.game_over_sprites)
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.pending_game = Snake()
            if event.type == pygame.QUIT:
                self.running = False

    async def run(self):
        while self.running:
            self.handle_events()
            screen.blit(self.bg_image, (0, 0))
            if self.score != None:
                self.game_over_sprites.update()
                self.score_text.update()
            else:
                self.menu_sprites.update()
            
            pygame.display.update()
            await asyncio.sleep(0)

            if self.pending_game:
                self.score = await self.pending_game.run()
                self.score_text = TextSprite(f'Final score: {self.score}', (WINDOW_WIDTH / 1.5, WINDOW_HEIGHT / 1.5), self.text_color, WINDOW_WIDTH / 24, ())
                self.pending_game = None