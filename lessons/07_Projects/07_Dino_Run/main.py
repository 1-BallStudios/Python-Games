"""
Dino Jump

Use the arrow keys to move the blue square up and down to avoid the black
obstacles. The game should end when the player collides with an obstacle ...
but it does not. It's a work in progress, and you'll have to finish it. 

"""
import pygame
import random
from pathlib import Path

# Initialize Pygame
pygame.init()

images_dir = Path(__file__).parent / "images" if (Path(__file__).parent / "images").exists() else Path(__file__).parent / "assets"

# Screen dimensions
WIDTH, HEIGHT = 600, 300
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dino Jump")

Score = 0
running = True
# Colors
WHITE = (255, 255, 255)
BLACK = (0,0,0)
RED = (255,0,0)

# FPS
FPS = 60

# Player attributes
PLAYER_SIZE = 35

player_speed = 5

# Obstacle attributes
OBSTACLE_WIDTH = 20
OBSTACLE_HEIGHT = 40
obstacle_speed = 5
high_score = 0

# Font
font = pygame.font.SysFont(None, 72, False, False)
font2 = pygame.font.SysFont(None, 120, False, False)


# Define an obstacle class
class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        
        self.image = pygame.Surface((OBSTACLE_WIDTH, OBSTACLE_HEIGHT))
        self.rect = self.image.get_rect()
        self.cactus = pygame.image.load(images_dir / "cactus_sheet.png")
        self.image = self.cactus
        self.image = pygame.transform.scale(self.image, (OBSTACLE_WIDTH, OBSTACLE_HEIGHT))
        self.rect = self.image.get_rect(center=self.rect.center)
        self.rect.x = WIDTH
        self.rect.y = HEIGHT - OBSTACLE_HEIGHT

        self.explosion = pygame.image.load(images_dir / "cactus_sheet.png")

    def update(self):
        global Score
        self.rect.x -= obstacle_speed
        # Remove the obstacle if it goes off screen
        if self.rect.right < 0:
            self.kill()

    def explode(self):
        """Replace the image with an explosition image."""
        
        # Load the explosion image
        self.image = self.explosion
        self.image = pygame.transform.scale(self.image, (OBSTACLE_WIDTH, OBSTACLE_HEIGHT))
        self.rect = self.image.get_rect(center=self.rect.center)
        


# Define a player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(images_dir / "dino_small_sheet.png"), (PLAYER_SIZE, PLAYER_SIZE))
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.y = HEIGHT - PLAYER_SIZE - 10
        self.speed = 0
        self.isjumping = 0

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.isjumping == 0: 
            self.speed = 15
            self.isjumping = 1


        # Keep the player on screen
        self.speed -= 1
        self.rect.y -= self.speed
 

        if self.rect.top < 0:
            self.rect.top = 0
            
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
            self.isjumping = 0
            self.speed = 0

# Create a player object
player = Player()
player_group = pygame.sprite.GroupSingle(player)

# Add obstacles periodically
def add_obstacle(obstacles): 
    if random.random() < 0.4:
        obstacle = Obstacle()
        obstacles.add(obstacle)
        return 1
    return 0


# Main game loop
def game_loop():
    global Score, running, obstacle_speed, high_score
    clock = pygame.time.Clock()
    game_over = False
    last_obstacle_time = pygame.time.get_ticks()
    prev_score = 0

    # Group for obstacles
    obstacles = pygame.sprite.Group()

    Score = 0
    obs_count = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                running = False

        # Update player
        if game_over == False:
            player_group.update()
            Score += 3
            if pygame.time.get_ticks() - last_obstacle_time > 500:
                last_obstacle_time = pygame.time.get_ticks()
                obs_count += add_obstacle(obstacles)
                keys = pygame.key.get_pressed()
            if Score >= prev_score + 1000:
                Score = prev_score + 1000
                prev_score = Score
                obstacle_speed += 1
        if game_over == False:
            obstacles.update()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r] and game_over == True:
            Score = 0
            prev_score = 0
            obstacles = pygame.sprite.Group()
            game_over = False
        


        # Check for collisions
        collider = pygame.sprite.spritecollide(player, obstacles, dokill=False)
        if collider:
            collider[0].explode()
            game_over = True
            if Score > high_score:
                high_score = Score
       
        # Draw everything
        screen.fill(WHITE)
        player_group.draw(screen)
        obstacles.draw(screen)
   
        # Display obstacle count
        score_text = font.render(f"{Score}", True, BLACK)
        screen.blit(score_text, (10, 10))
        score_text = font.render(f"High: {high_score}", True, BLACK)
        screen.blit(score_text, (310, 10))
        game_over_text = font2.render("GAME OVER", True, RED)
        game_over_text2 = font.render("Press R to Try Again", True, BLACK)
        if game_over == True:
            screen.blit(game_over_text, (60, 100))
            screen.blit(game_over_text2, (60, 200))

        pygame.display.update()
        clock.tick(FPS)

    # Game over screen
    screen.fill(WHITE)

if __name__ == "__main__":
    game_loop()
