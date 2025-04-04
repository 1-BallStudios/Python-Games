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
bulletcount = 0
enemycount = 0
last_bullet_time = 0
lemt = 0
Score = 0
WHITE = (255,255,255)
RED = (255,0,0)
bullet_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
font = pygame.font.SysFont(None, 72, False, False)
font2 = pygame.font.SysFont(None, 120, False, False)
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Space Invaders')

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

def add_bullet(bullets, x):
    bullet = Bullet(x)
    bullets.add(bullet) 
    return 1

def add_enemy(enemies, x, y):
    enemy = Enemy(x, y)
    enemies.add(enemy) 
    return 1

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
        global bulletcount, last_bullet_time
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]: 
            self.speed = -1
        elif keys[pygame.K_RIGHT]: 
            self.speed = 1
        else: 
            self.speed = 0
        
        if keys[pygame.K_SPACE] and bulletcount < 3 and pygame.time.get_ticks() > last_bullet_time + 200:
            bulletcount += add_bullet(bullet_group, self.rect.x + 10)
            last_bullet_time = pygame.time.get_ticks()

        self.rect.x += self.speed

player = Player()
player_group = pygame.sprite.GroupSingle(player)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x):
        super().__init__()
        self.image = pygame.Surface((18,28))
        self.rect = self.image.get_rect()
        self.proj = pygame.image.load(images/"projectile.png")
        self.image = self.proj
        self.image = pygame.transform.scale(self.image, (18,28))
        self.rect = self.image.get_rect(center=self.rect.center)
        self.rect.x = x
        self.rect.y = 500
        self.speed = 0

    def update(self):
        global bulletcount
        self.rect.y -= 2
        if self.rect.y < 0:
            bulletcount -= 1
            self.kill()
        

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((50,40))
        self.rect = self.image.get_rect()
        self.enemy = pygame.image.load(images/"alien.png")
        self.image = self.enemy
        self.image = pygame.transform.scale(self.image, (50,40))
        self.rect = self.image.get_rect(center=self.rect.center)
        self.rect.x = x
        self.rect.y = y
        self.speed = 0.5
        self.lemt = 0

    def update(self):
        global Score
        if True:
            self.rect.x += self.speed
        if self.rect.x >= 550 or self.rect.x <= 0:
            self.speed = self.speed * -1
            self.rect.y += 20
        self.lemt = pygame.time.get_ticks()
        collider2 = pygame.sprite.spritecollide(self, bullet_group, dokill=False)
        if collider2:
            Score += 100
            self.kill()
        
clock = pygame.time.Clock()
running = True
game_over = False
background = make_tiled_bg(screen, images/"space.png")

x = 30
y = 80
for i in range(3):
    for i in range(7):
        enemycount += add_enemy(enemy_group, x, y)
        x += 80
    x = 30
    y += 60

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    player_group.update()
    enemy_group.update()
    bullet_group.update()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_r] and game_over == True:
        Score = 0
        game_over = False
        bullet_group = pygame.sprite.Group()
        enemy_group = pygame.sprite.Group()

    screen.blit(background,(0,0))
    player_group.draw(screen)
    bullet_group.draw(screen)
    enemy_group.draw(screen)
    score_text = font.render(f"{Score}", True, WHITE)
    game_over_text = font2.render("GAME OVER", True, RED)
    game_over_text2 = font.render("Press R to Try Again", True, WHITE)
    screen.blit(score_text, ((300 - (((len(str(Score)) - 1) / 2) * 36)), 10))
    if game_over == True:
        screen.blit(game_over_text, (60, 100))
        screen.blit(game_over_text2, (60, 300 ))

    # Update the display
    pygame.display.flip()
# Quit Pygame
pygame.quit()