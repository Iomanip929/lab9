import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Game constants
WIDTH, HEIGHT = 600, 600
CELL_SIZE = 20  # Size of one cell
SNAKE_COLOR = (0, 255, 0)
FOOD_COLOR = (255, 0, 0)
BACKGROUND_COLOR = (0, 0, 0)
TEXT_COLOR = (255, 255, 255)

# Create game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# Game speed and level settings
speed = 10
level = 1
score = 0

# Initial snake position
snake = [(WIDTH // 2, HEIGHT // 2)]
snake_direction = (CELL_SIZE, 0)

# Food variables
food = None
food_timer = None
food_value = 1  # Default food value

# Function to generate food at a random position with different values
def generate_food():
    global food_timer, food_value
    while True:
        food_x = random.randint(0, (WIDTH // CELL_SIZE) - 1) * CELL_SIZE
        food_y = random.randint(0, (HEIGHT // CELL_SIZE) - 1) * CELL_SIZE
        if (food_x, food_y) not in snake:
            food_value = random.choice([1, 2, 3])
            food_timer = time.time()
            return food_x, food_y

# Generate the first food
food = generate_food()

# Font for score and level display
font = pygame.font.SysFont("Verdana", 20)

# Game loop
running = True
while running:
    pygame.time.delay(1000 // speed)  # Control snake speed

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Snake movement control
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and snake_direction != (0, CELL_SIZE):  
        snake_direction = (0, -CELL_SIZE)
    if keys[pygame.K_DOWN] and snake_direction != (0, -CELL_SIZE):  
        snake_direction = (0, CELL_SIZE)
    if keys[pygame.K_LEFT] and snake_direction != (CELL_SIZE, 0):  
        snake_direction = (-CELL_SIZE, 0)
    if keys[pygame.K_RIGHT] and snake_direction != (-CELL_SIZE, 0):  
        snake_direction = (CELL_SIZE, 0)

    # Move the snake
    new_head = (snake[0][0] + snake_direction[0], snake[0][1] + snake_direction[1])

    # Check for wall collision
    if new_head[0] < 0 or new_head[0] >= WIDTH or new_head[1] < 0 or new_head[1] >= HEIGHT:
        print("Game Over! The snake hit the wall.")
        running = False

    # Check for self-collision
    if new_head in snake:
        print("Game Over! The snake hit itself.")
        running = False

    # Add new head to the snake
    snake.insert(0, new_head)

    # Check if food disappears after some time
    if food and time.time() - food_timer > 5:  # Food disappears after 5 seconds
        food = generate_food()

    # Check if snake eats food
    if new_head == food:
        score += food_value
        food = generate_food()  # Generate new food
        if score % 3 == 0:
            level += 1
            speed += 2
    else:
        snake.pop()  # If no food eaten, remove the last segment

    # Draw everything
    screen.fill(BACKGROUND_COLOR)
    
    # Draw the snake
    for segment in snake:
        pygame.draw.rect(screen, SNAKE_COLOR, (segment[0], segment[1], CELL_SIZE, CELL_SIZE))

    # Draw the food if available
    if food:
        pygame.draw.rect(screen, FOOD_COLOR, (food[0], food[1], CELL_SIZE, CELL_SIZE))
    
    # Display score and level
    score_text = font.render(f"Score: {score}", True, TEXT_COLOR)
    level_text = font.render(f"Level: {level}", True, TEXT_COLOR)
    screen.blit(score_text, (10, 10))
    screen.blit(level_text, (10, 40))

    # Update the screen
    pygame.display.update()

# Quit the game
pygame.quit()