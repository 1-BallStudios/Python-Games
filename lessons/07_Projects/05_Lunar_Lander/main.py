import pygame
import random
import math
from pathlib import Path

pygame.init()

images = Path(__file__).parent / "images"

class Settings:
    screen_width = 600
    screen_height = 600
    fps = 60
    BLACK = (0,0,0)
    RED = (255,0,0)
    YELLOW = (255,255,0)
    GREEN = (0,255,0)
    WHITE = (255,255,255)
    screen = pygame.display.set_mode((screen_width, screen_height))
    font = pygame.font.SysFont(None, 50, False, False)
    font2 = pygame.font.SysFont(None, 120, False, False)
    pygame.display.set_caption('Asteroids')

fuel = 100
score = 0

def groundify(x):
    if x <= 100:
        return 480
    elif x <= 200:
        return 480 + 0.4 * (x - 100)
    elif x <= 400:
        return 520
    elif x <= 440:
        return 520 - 3 * (x - 400)
    elif x <= 480:
        return 400 + 3 * (x - 440)
    elif x <= 540:
        return 520
    else:
        return 520 - (1/3) * (x - 520)

class Player(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        self.original_image = self.create_spaceship_image()
        self.velocity = pygame.Vector2(0, 0)
        self.pos = pygame.Vector2(300,100)
        self.image = self.original_image.copy() 
        self.rect = self.image.get_rect(center=position)
        self.last_shot = pygame.time.get_ticks()
        self.angle = 0
        self.shoot_delay = 250  

    def create_spaceship_image(self):
        image = pygame.Surface( (40, 40),pygame.SRCALPHA)
        points = [
            (20, 0),  # top point
            (5, 50),  # left side point
            (35, 50),  # right side point
        ]
        pygame.draw.polygon(image, Settings.WHITE, points)
        return image

    def update(self):
        self.velocity.y+=0.01
        global fuel
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.angle -= 5

        if keys[pygame.K_RIGHT]:
            self.angle += 5

        if keys[pygame.K_UP]:
            if fuel > 0:
                self.velocity = pygame.Vector2(0, -2).rotate(self.angle)
                fuel -= 0.5

        self.velocity = self.velocity * 0.99

        self.image = pygame.transform.rotate(self.original_image, -self.angle)

        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        ground_y = groundify(self.pos.x)
        if self.rect.bottom >= ground_y:
            self.rect.bottom = ground_y

class Game:
    def __init__(self, settings):
        pygame.init()
        pygame.key.set_repeat(1250, 1250)
        self.clock = pygame.time.Clock()
        self.running = True
        self.all_sprites = pygame.sprite.Group()

    def add(self, sprite):
        sprite.game = self
        self.all_sprites.add(sprite)
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update(self):
        self.all_sprites.update()

    def draw(self):
        global score
        Settings.screen.fill(Settings.BLACK)
        self.all_sprites.draw(Settings.screen)
        points2 = [
            (10, 50),  # top point
            (50, 50),  # left side point
            (50, 75),
            (10, 75),  # right side point
        ]
        pygame.draw.polygon(Settings.screen, Settings.RED, points2)
        points2 = [
            (50, 50),  # top point
            (100, 50),  # left side point
            (100, 75),
            (50, 75),  # right side point
        ]
        pygame.draw.polygon(Settings.screen, Settings.YELLOW, points2)
        points2 = [
            (100, 50),  # top point
            (210, 50),  # left side point
            (210, 75),
            (100, 75),  # right side point
        ]
        pygame.draw.polygon(Settings.screen, Settings.GREEN, points2)
        points2 = [
            ((fuel*2+10), 40),  # top point
            ((fuel*2+20), 40),  # left side point
            ((fuel*2+20), 85),
            ((fuel*2+10), 85),  # right side point
        ]
        pygame.draw.polygon(Settings.screen, Settings.WHITE, points2)
        points3 = [
            (-10, 600),
            (-10, 480),
            (100, 480),
            (200, 520),
            (400, 520),
            (440, 400),
            (480, 520),
            (540, 520),
            (600, 500),
            (600, 600),
        ]
        pygame.draw.polygon(Settings.screen, Settings.WHITE, points3, 3)
        fuel_text = Settings.font.render(f"FUEL", True, Settings.WHITE)
        Settings.screen.blit(fuel_text, (10, 10))
        fuel_text = Settings.font.render(f"{score}", True, Settings.GREEN)
        Settings.screen.blit(fuel_text, (300, 10))

        pygame.display.flip()

    def run(self):
        global last_ast_time, obs_count
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(Settings.fps)
        pygame.quit()

if __name__ == "__main__":

    game = Game(Settings)
    spaceship = Player(
        position=(300,100)
    )

    game.add(spaceship)

    game.run()
