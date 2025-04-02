#Imports
import pygame, sys
from pygame.locals import *
import random, time

# Initializing
pygame.init()

# Setting up FPS
FPS = 60
FramePerSec = pygame.time.Clock()

# Colors
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Game Variables
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SPEED = 5  # Initial speed of enemies
SCORE = 0
COUNT_COIN = 0  # Number of collected coins
COIN_THRESHOLD = 5  # Number of coins to increase speed

# Fonts
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, BLACK)

# Load Background
background = pygame.image.load("c:\Program Files (x86)\lab_saves\AnimatedStreet.png")

# Create Screen
display_surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
display_surface.fill(WHITE)
pygame.display.set_caption("Racing Game")

# Enemy Class
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("c:\Program Files (x86)\lab_saves\Enemy (1).png")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

    def move(self):
        global SCORE
        self.rect.move_ip(0, SPEED)
        if self.rect.bottom > SCREEN_HEIGHT:
            SCORE += 1
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

# Player Class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("c:\Program Files (x86)\lab_saves\player (1).png")
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)

    def move(self):
        pressed_keys = pygame.key.get_pressed()
        if self.rect.left > 0 and pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if self.rect.right < SCREEN_WIDTH and pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)

# Coin Class with Different Values
class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("c:\Program Files (x86)\lab_saves\coin.png")
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), random.randint(50, 300))
        self.value = random.choice([1, 2, 3])  # Coin values: 1, 2, or 3 points

    def move(self):
        self.rect.move_ip(0, SPEED)
        if self.rect.top > SCREEN_HEIGHT:
            self.reset_position()

    def reset_position(self):
        self.rect.top = random.randint(-100, -30)
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), self.rect.top)
        self.value = random.choice([1, 2, 3])  # Assign new random value

# Creating Sprites
P1 = Player()
E1 = Enemy()
C1 = Coin()

# Creating Sprite Groups
enemies = pygame.sprite.Group()
enemies.add(E1)

coins = pygame.sprite.Group()
coins.add(C1)

all_sprites = pygame.sprite.Group()
all_sprites.add(P1, E1, C1)

# Speed Increase Event
INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)

# Game Loop
while True:
    for event in pygame.event.get():
        if event.type == INC_SPEED:
            SPEED += 0.5  # Gradually increase speed
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    display_surface.blit(background, (0, 0))

    # Display Score
    scores = font_small.render(str(SCORE), True, BLACK)
    display_surface.blit(scores, (10, 10))

    # Display Collected Coins
    coin_score = font_small.render("Coins: " + str(COUNT_COIN), True, BLACK)
    display_surface.blit(coin_score, (SCREEN_WIDTH - 100, 10))

    # Move and Redraw all Sprites
    for entity in all_sprites:
        entity.move()
        display_surface.blit(entity.image, entity.rect)

    # Check for collision with Enemy
    if pygame.sprite.spritecollideany(P1, enemies):
        pygame.mixer.Sound('c:\Program Files (x86)\lab_saves\crash.wav').play()
        time.sleep(1)
        display_surface.fill(RED)
        display_surface.blit(game_over, (30, 250))
        pygame.display.update()
        for entity in all_sprites:
            entity.kill()
        time.sleep(2)
        pygame.quit()
        sys.exit()

    # Check for collision with Coin
    for coin in coins:
        if P1.rect.colliderect(coin.rect):
            COUNT_COIN += coin.value  # Increase count by coin's value
            coin.reset_position()

            # Increase enemy speed after collecting a set number of coins
            if COUNT_COIN % COIN_THRESHOLD == 0:
                SPEED += 1

    pygame.display.update()
    FramePerSec.tick(FPS)