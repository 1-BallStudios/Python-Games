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
Level = 1
furthest_enemy_pos = 510
direction = 1
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
YELLOW = (255,255,0)
ORANGE = (255,128,0)
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

def add_enemy(enemies, x, y, id):
    enemy = Enemy(x, y, id)
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
    def __init__(self, x, y, ID):
        super().__init__()
        self.image = pygame.Surface((50,40))
        self.rect = self.image.get_rect()
        self.enemy = pygame.image.load(images/"alien.png")
        self.image = self.enemy
        self.image = pygame.transform.scale(self.image, (50,40))
        self.rect = self.image.get_rect(center=self.rect.center)
        self.rect.x = x
        self.rect.y = y
        self.ID = ID
        self.speed = 2
        self.lemt = 0

    def update(self):
        global Score, bulletcount, game_over
        self.lemt = pygame.time.get_ticks()
        collider2 = pygame.sprite.spritecollide(self, bullet_group, dokill=False)
        if collider2:
            Score += 100
            self.kill()
            collider2[0].kill()
            bulletcount -= 1
        collider3 = pygame.sprite.spritecollide(self, player_group, dokill=False)
        if collider3:
            game_over = True

    def move(self):
        global furthest_enemy_pos, direction

        self.rect.x += self.speed

    def cfd(self):
        global furthest_enemy_pos, direction

        if furthest_enemy_pos >= 550 or furthest_enemy_pos <= 480:
            self.rect.y += 20
            self.speed = self.speed * -1
            self.rect.x += self.speed * 3
  
            
        
clock = pygame.time.Clock()
running = True
game_over = False
background = make_tiled_bg(screen, images/"space.png")

lmt = 0
x = 30
y = 80
id = 1
for i in range(3):
    for i in range(7):
        enemycount += add_enemy(enemy_group, x, y, id)
        x += 80
        id += 1
    x = 30
    y += 60

while pygame.time.get_ticks() < 1000:
    count_text = font2.render("3", True, YELLOW)
    screen.blit(background,(0,0))
    screen.blit(count_text, (300, 300))
    pygame.display.flip()
while pygame.time.get_ticks() < 2000:
    count_text = font2.render("2", True, ORANGE)
    screen.blit(background,(0,0))
    screen.blit(count_text, (300, 300))
    pygame.display.flip()
while pygame.time.get_ticks() < 3000:
    count_text = font2.render("1", True, RED)
    screen.blit(background,(0,0))
    screen.blit(count_text, (300, 300))
    pygame.display.flip()
while pygame.time.get_ticks() < 4000:
    count_text = font2.render("GO!", True, GREEN)
    screen.blit(background,(0,0))
    screen.blit(count_text, (250, 300))
    pygame.display.flip()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    player_group.update()
    enemy_group.update()
    bullet_group.update()

    if pygame.time.get_ticks() > lmt + 500:
        lmt = pygame.time.get_ticks()
        for e in enemy_group:
            e.move()
            e.cfd()
        furthest_enemy_pos += direction * 2
        if furthest_enemy_pos >= 550 or furthest_enemy_pos <= 480:
            direction = direction * -1

    keys = pygame.key.get_pressed()
    if (keys[pygame.K_r] and game_over == True) or (Score % 2100 == 0 and Score > 0):
        if game_over == True:
            Score = 0
        else:
            Level += 1
        game_over = False
        bullet_group = pygame.sprite.Group()
        enemy_group = pygame.sprite.Group()
        furthest_enemy_pos = 510
        x = 30
        y = 80
        id = 1
        for i in range(3):
            for i in range(7):
                enemycount += add_enemy(enemy_group, x, y, id)
                x += 80
                id += 1
            x = 30
            y += 60


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
        screen.blit(game_over_text2, (60, 300))

    # Update the display
    pygame.display.flip()
# Quit Pygame
pygame.quit()