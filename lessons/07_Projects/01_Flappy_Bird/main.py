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
Score = 0
game_over = False
obs_count = 0
WHITE = (255, 255, 255)
BLACK = (0,0,0)
RED = (255,0,0)
font = pygame.font.SysFont(None, 72, False, False)
font2 = pygame.font.SysFont(None, 120, False, False)
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Flappy Bird')

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

class Bird(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((51,36))
        self.rect = self.image.get_rect()
        self.bird = pygame.image.load(images/"bluebird-midflap.png")
        self.image = self.bird
        self.image = pygame.transform.scale(self.image, (51,36))
        self.rect = self.image.get_rect(center=self.rect.center)
        self.rect.x = 300
        self.rect.y = 300
        self.speed = 0

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]: 
            self.speed = 2
        
        self.speed -= 0.05
        self.rect.y -= self.speed

    def reset(self):
        self.speed = 0
        self.rect.y = 300

class Pipe(pygame.sprite.Sprite):
    def __init__(self, is_inverted, y):
        super().__init__()
        self.image = pygame.Surface((60,400))
        self.rect = self.image.get_rect()
        self.pipe = pygame.image.load(images/"pipe-green.png")
        self.image = self.pipe
        self.image = pygame.transform.scale(self.image, (60,400))
        if is_inverted == True:
            self.image = pygame.transform.flip(self.image, False, True)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.rect.x = 600
        self.rect.y = y
        self.inverted = is_inverted

    def update(self):
        global Score
        self.rect.x -= 2
        # Remove the obstacle if it goes off screen
        if self.rect.right == 300:
            if self.inverted == False:
                Score += 1

        if self.rect.right < 0:
            self.kill()

def add_pipe(pipes):
    pipe_y = random.randint(150,500)
    pipe = Pipe(False, pipe_y)
    pipes.add(pipe)
    pipe = Pipe(True, pipe_y - 600)
    pipes.add(pipe)
    return 1

background = make_tiled_bg(screen, images/"background.png")
bird = Bird()
bird_group = pygame.sprite.GroupSingle(bird)

# Main loop
clock = pygame.time.Clock()
last_pipe_time = pygame.time.get_ticks()
running = True
game_over = False
pipe_group = pygame.sprite.Group()
game_over_time = 0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if game_over == False:
        bird_group.update()

    if game_over == False:
        pipe_group.update()
    
    collider = pygame.sprite.spritecollide(bird, pipe_group, dokill=False)
    if collider or bird.rect.y > 600:
        if game_over == False:
            game_over_time = pygame.time.get_ticks()
        game_over = True
        #game_over_countdown = 5 - math.floor((pygame.time.get_ticks() - game_over_time) / 1000)

    if pygame.time.get_ticks() - last_pipe_time > 1000 and game_over == False:
        last_pipe_time = pygame.time.get_ticks()
        obs_count += add_pipe(pipe_group)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_r] and game_over == True:
        Score = 0
        bird.reset()
        game_over = False
        pipe_group = pygame.sprite.Group()
        

    screen.blit(background,(0,0))
    bird_group.draw(screen)
    pipe_group.draw(screen)
    score_text = font.render(f"{Score}", True, BLACK)
    game_over_text = font2.render("GAME OVER", True, RED)
    game_over_text2 = font.render("Press R to Try Again", True, BLACK)
    screen.blit(score_text, ((300 - (((len(str(Score)) - 1) / 2) * 36)), 10))
    if game_over == True:
        screen.blit(game_over_text, (60, 100))
        screen.blit(game_over_text2, (60, 300 ))

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()