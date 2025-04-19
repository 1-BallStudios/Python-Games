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
lmt = 0
font = pygame.font.SysFont(None, 72, False, False)
font2 = pygame.font.SysFont(None, 120, False, False)
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Frogger')

def make_tiled_bg(screen, bg_file):
    # Scale background to match the screen height
    
    bg_tile = pygame.image.load(bg_file).convert()
    
    background_height = screen.get_height()
    bg_tile = pygame.transform.scale(bg_tile, (bg_tile.get_width(), screen.get_height()))

    # Get the dimensions of the background after scaling
    background_width = bg_tile.get_width()

    # Make an image the is the same size as the screen
    image = pygame.Surface((screen.get_width(), screen.get_height()))

    # Tile the background image in the x-direction
    for x in range(0, screen.get_width(), background_width):
        image.blit(bg_tile, (x, 0))

    return image

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40,48))
        self.rect = self.image.get_rect()
        self.rocket = pygame.image.load(images/"frog.png")
        self.image = self.rocket
        self.image = pygame.transform.scale(self.image, (40,48))
        self.rect = self.image.get_rect(center=self.rect.center)
        self.rect.x = 300
        self.rect.y = 500
        self.vX = 0
        self.vY = 0
    
    def update(self):
        global lmt
        keys = pygame.key.get_pressed()
        if pygame.time.get_ticks() > lmt + 200:
            
            if keys[pygame.K_UP]: 
                self.vY = -32
                lmt = pygame.time.get_ticks()
            elif keys[pygame.K_DOWN]: 
                self.vY = 32
                lmt = pygame.time.get_ticks()
            elif keys[pygame.K_LEFT]: 
                self.vX = -32
                lmt = pygame.time.get_ticks()
            elif keys[pygame.K_RIGHT]: 
                self.vX = 32
                lmt = pygame.time.get_ticks()
        else: 
            self.vX = 0
            self.vY = 0
        
        self.rect.x += self.vX
        self.rect.y += self.vY

player = Player()
player_group = pygame.sprite.GroupSingle(player)

clock = pygame.time.Clock()
running = True
game_over = False
background = make_tiled_bg(screen, images/"frogger_road_bg.png")
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    player_group.update()

    screen.blit(background,(0,0))
    player_group.draw(screen)

    # Update the display
    pygame.display.flip()
# Quit Pygame
pygame.quit()