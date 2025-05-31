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
    shoot_delay = 250
    BLACK = (0,0,0)
    RED = (255,0,0)
    WHITE = (255,255,255)
    screen = pygame.display.set_mode((screen_width, screen_height))
    font = pygame.font.SysFont(None, 50, False, False)
    font2 = pygame.font.SysFont(None, 120, False, False)
    pygame.display.set_caption('Tank War')

class Player(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        self.original_image = self.create_spaceship_image()
        self.velocity = pygame.Vector2(0, 0)
        self.pos = pygame.Vector2(300,300)
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

    def fire_projectile(self):
        global proj_group
        new_projectile = Projectile(
            position=self.rect.center,
            angle=self.angle,
            velocity=5,
        )
        proj_group.add(new_projectile)

    def ready_to_shoot(self):
        if pygame.time.get_ticks() - self.last_shot > self.shoot_delay:
            self.last_shot = pygame.time.get_ticks()
            return True
        return False
            
        

    def update(self):
        
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.angle -= 5

        if keys[pygame.K_RIGHT]:
            self.angle += 5

        if keys[pygame.K_UP]:
            self.velocity = pygame.Vector2(0, -2).rotate(self.angle)

        self.velocity = self.velocity * 0.99

        if keys[pygame.K_SPACE] and self.ready_to_shoot():
            self.fire_projectile()

        self.image = pygame.transform.rotate(self.original_image, -self.angle)

        self.pos += self.velocity
        if self.pos.x < 0:
            self.pos.x = 800
        if self.pos.x > 800:
            self.pos.x = 0
        if self.pos.y < 0:
            self.pos.y = 800
        if self.pos.y > 800:
            self.pos.y = 0
        self.rect = self.image.get_rect(center=self.rect.center)
        
        self.rect.center = self.pos
    
        super().update()

class Projectile(pygame.sprite.Sprite):
    def __init__(self, position, velocity, angle):
        super().__init__()
        self.original_image = self.create_spaceship_image(position)
        self.image = self.original_image.copy() 
        self.rect = self.image.get_rect(center=position)

        self.velocity = pygame.Vector2(0, -1).rotate(angle) * velocity
        print(self.rect)

    def create_spaceship_image(self, position):
        image = pygame.Surface( (position[0], position[1]),pygame.SRCALPHA)
        points2 = [
            (10, 10),  # top point
            (-10, 10),  # left side point
            (-10, -10),  # right side point
            (10, -10),  # right side point
        ]
        pygame.draw.polygon(image, Settings.WHITE, points2)
        
        return image
    
    def update(self):
        self.rect.center += self.velocity
        
proj_group = pygame.sprite.Group()
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
        Settings.screen.fill(Settings.BLACK)
        self.all_sprites.draw(Settings.screen)

        pygame.display.flip()

    def run(self):
        global last_ast_time, obs_count
        while self.running:
            self.handle_events()
            self.update()
            proj_group.update()
            self.draw()
            proj_group.draw(Settings.screen)
            self.clock.tick(Settings.fps)
        pygame.quit()

if __name__ == "__main__":

    game = Game(Settings)
    spaceship = Player(
        position=(300,300)
    )

    game.add(spaceship)

    game.run()
