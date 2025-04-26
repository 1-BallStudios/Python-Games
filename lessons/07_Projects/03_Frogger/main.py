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
Score = 99
Level = 1
Lives = 3
MaxScore = 99
last_car_time = 0
BLACK = (0,0,0)
RED = (255,0,0)
font = pygame.font.SysFont(None, 50, False, False)
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
        self.image = pygame.Surface((32,32))
        self.rect = self.image.get_rect()
        self.rocket = pygame.image.load(images/"frog.png")
        self.image = self.rocket
        self.image = pygame.transform.scale(self.image, (32,32))
        self.rect = self.image.get_rect(center=self.rect.center)
        self.rect.x = 300
        self.rect.y = 520
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

    def reset(self):
        self.rect.x = 300
        self.rect.y = 520
        self.vX = 0
        self.vY = 0

player = Player()
player_group = pygame.sprite.GroupSingle(player)

class Car(pygame.sprite.Sprite):
    def __init__(self, y):
        super().__init__()
        self.image = pygame.Surface((100,70))
        self.rect = self.image.get_rect()
        self.car = pygame.image.load(images/"carLeft.png")
        self.image = self.car
        self.image = pygame.transform.scale(self.image, (100,70))
        self.rect = self.image.get_rect(center=self.rect.center)
        self.rect.x = 600
        self.rect.y = y

    def update(self):
        global Level
        self.rect.x -= (2 + (Level / 4))
        if self.rect.right < 0:
            self.kill()
        

def add_car(cars):
    car_y = 150 + (random.randint(0,4) * 70)
    car = Car(car_y)
    cars.add(car)
    return 1

clock = pygame.time.Clock()
running = True
game_over = False
obs_count = 0
car_group = pygame.sprite.Group()
background = make_tiled_bg(screen, images/"frogger_road_bg.png")
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    collider = pygame.sprite.spritecollide(player, car_group, dokill=False)
    if collider:
        if Lives > 0:
            Lives -= 1
        if Lives < 1:
            game_over = True
        else:
            game_over = False
            player.reset()
            car_group = pygame.sprite.Group()
            Score = MaxScore
            

    if game_over == False:
        player_group.update()
        car_group.update()

    if player.rect.y <= 100:
        Level += 1
        MaxScore = Score + 99
        Score += 99
        
        player.reset()
        car_group = pygame.sprite.Group()

    if pygame.time.get_ticks() - last_car_time > 1000 and game_over == False:
        last_car_time = pygame.time.get_ticks()
        obs_count += add_car(car_group)
        if Score > MaxScore - 99:
            Score -= 1
    keys = pygame.key.get_pressed()
    if keys[pygame.K_r] and game_over == True:
        game_over = False
        player.reset()
        car_group = pygame.sprite.Group()
        Score = 99
        MaxScore = 99
        Level = 1
        Lives = 3

    screen.blit(background,(0,0))
    player_group.draw(screen)
    car_group.draw(screen)
    score_text = font.render(f"Score: {Score} / {MaxScore}", True, BLACK)
    lives_text = font.render(f"Lives: {Lives}", True, BLACK)
    level_text = font.render(f"Level {Level}", True, BLACK)
    game_over_text = font2.render("GAME OVER", True, RED)
    game_over_text2 = font.render("Press R to Try Again", True, BLACK)
    screen.blit(score_text, (10, 10))
    screen.blit(lives_text, (310, 10))
    screen.blit(level_text, (470, 10))
    if game_over == True:
        screen.blit(game_over_text, (60, 100))
        screen.blit(game_over_text2, (60, 300 ))

    # Update the display
    pygame.display.flip()
# Quit Pygame
pygame.quit()