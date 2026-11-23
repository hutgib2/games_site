from game.settings import *
from game.roguelike import Roguelike
from game.textSprite import TextSprite
import asyncio

class Menu:
    def __init__(self):
        self.bg_image = pygame.image.load('assets/images/roguelike.png')
        self.bg_image = pygame.transform.smoothscale(self.bg_image, (WINDOW_WIDTH, WINDOW_HEIGHT))
        self.pending_game = None
        self.running = True
        self.menu_sprites = pygame.sprite.Group()
        self.game_over_sprites = pygame.sprite.Group()
        self.score = None
        self.text_color = (255, 255, 255)
        self.game_over_color = (128, 0, 0)
        self.title_size = WINDOW_WIDTH / 12
        self.paragraph_size = WINDOW_WIDTH / 24
        TextSprite("Welcome to Mr. Roguelike!", (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 6), self.text_color, self.title_size, self.menu_sprites)
        TextSprite("Press P to play", (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 1.2), self.text_color, self.paragraph_size, (self.menu_sprites, self.game_over_sprites))
        TextSprite('Game Over', (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 6), self.game_over_color, self.title_size, self.game_over_sprites)
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    self.pending_game = Roguelike()
            if event.type == pygame.QUIT:
                self.running = False

    async def run(self):
        while self.running:
            self.handle_events()
            screen.fill((0, 0, 0))
            screen.blit(self.bg_image, (0, 100))
            if self.score != None:
                self.game_over_sprites.update()
                self.score_text.update()
            else:
                self.menu_sprites.update()
            
            pygame.display.update()
            await asyncio.sleep(0)

            if self.pending_game:
                self.score = await self.pending_game.run()
                self.score_text = TextSprite(f'Final score: {self.score}', (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 3), self.game_over_color, self.paragraph_size, ())
                self.pending_game = None