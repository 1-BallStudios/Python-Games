import pygame
import random
import math
from pathlib import Path

pygame.init()

images = Path(__file__).parent / "images"

next_ID = 0
p1_hp = 100
p2_hp = 100

class Settings:
    screen_width = 600
    screen_height = 600
    fps = 60
    shoot_delay = 250
    BLACK = (0,0,0)
    RED = (255,0,0)
    GREEN = (0,255,0)
    WHITE = (255,255,255)
    screen = pygame.display.set_mode((screen_width, screen_height))
    font = pygame.font.SysFont(None, 50, False, False)
    font2 = pygame.font.SysFont(None, 120, False, False)
    pygame.display.set_caption('Tank War')

class Player(pygame.sprite.Sprite):
    def __init__(self, position, angle):
        super().__init__()
        global next_ID
        self.id = next_ID
        next_ID += 1
        self.original_image = self.create_spaceship_image()
        self.velocity = pygame.Vector2(0, 0)
        self.pos = position
        self.image = self.original_image.copy() 
        self.rect = self.image.get_rect(center=position)
        self.last_shot = pygame.time.get_ticks()
        self.angle = angle
        self.shoot_delay = 250  

    def create_spaceship_image(self):
        image = pygame.Surface( (50, 50),pygame.SRCALPHA)
        points = [
            (0, 10),
            (10, 10),
            (10, 20),
            (15, 20),
            (15, 0),
            (25, 0),
            (25, 20),
            (30, 20),
            (30, 10),
            (40, 10),
            (40, 40),
            (30, 40),
            (30, 35),
            (10, 35),
            (10, 40),
            (0, 40)
        ]
        if self.id == 0:
            pygame.draw.polygon(image, Settings.RED, points)
        else:
            pygame.draw.polygon(image, Settings.GREEN, points)
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
        global p1_hp, p2_hp
        keys = pygame.key.get_pressed()

        if self.id == 0 and keys[pygame.K_LEFT] or self.id == 1 and keys[pygame.K_a]:
            self.angle -= 5

        if self.id == 0 and keys[pygame.K_RIGHT] or self.id == 1 and keys[pygame.K_d]:
            self.angle += 5

        if self.id == 0 and keys[pygame.K_UP] or self.id == 1 and keys[pygame.K_w]:
            self.velocity = pygame.Vector2(0, -2).rotate(self.angle)
        else:
            self.velocity = pygame.Vector2(0, 0)

        if self.id == 0:
            if keys[pygame.K_DOWN] and self.ready_to_shoot():
                self.fire_projectile()
        else:
            if keys[pygame.K_s] and self.ready_to_shoot():
                self.fire_projectile()

        self.image = pygame.transform.rotate(self.original_image, -self.angle)

        self.pos += self.velocity
        self.rect = self.image.get_rect(center=self.rect.center)
        
        self.rect.center = self.pos

        collider = pygame.sprite.spritecollide(self, proj_group, dokill=False)
        if collider:
            if self.id == 0:
                p1_hp -= 0.5
            else:
                p2_hp -= 0.5
    
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
        fuel_text = Settings.font.render(f"{p1_hp}", True, Settings.RED)
        Settings.screen.blit(fuel_text, (10, 10))
        fuel_text = Settings.font.render(f"{p2_hp}", True, Settings.GREEN)
        Settings.screen.blit(fuel_text, (510, 10))
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
        position=(100,300),
        angle = 90
    )
    spaceship2 = Player(
        position=(500,300),
        angle = -90
    )

    game.add(spaceship)
    game.add(spaceship2)

    game.run()
