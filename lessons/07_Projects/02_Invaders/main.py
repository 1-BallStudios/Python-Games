import pygame
import random
import math

# Initialize Pygame
pygame.init()

from pathlib import Path
images = Path(__file__).parent / 'images'

# Set up display
screen_width = 600
screen_height = 600
font = pygame.font.SysFont(None, 72, False, False)
font2 = pygame.font.SysFont(None, 120, False, False)
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Space Invaders')
                           
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40,48))
        self.rect = self.image.get_rect()
        self.rocket = pygame.image.load(images/"rocket.png")
        self.image = self.rocket
        self.image = pygame.transform.scale(self.image, (40,48))
        self.rect = self.image.get_rect(center=self.rect.center)
        self.rect.x = 300
        self.rect.y = 500
        self.speed = 0

        
        
    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]: 
            self.speed = -1
        elif keys[pygame.K_RIGHT]: 
            self.speed = 1
        else: 
            self.speed = 0
        
        self.rect.x += self.speed

player = Player()
player_group = pygame.sprite.GroupSingle(player)

clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    player_group.update()

    player_group.draw(screen)

    # Update the display
    pygame.display.flip()
# Quit Pygame
pygame.quit()