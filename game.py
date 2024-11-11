import pygame
import random

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ball Collecting Coins Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GOLD = (255, 215, 0)

# Ball properties
ball_radius = 20
ball_speed = 5

# Coin properties
coin_radius = 10

# Game settings
target_score = 10  # Coins needed to win
time_limit = 30  # Time limit in seconds
reset_delay = 3000  # 3 seconds in milliseconds

# Font
font = pygame.font.Font(None, 36)

# Reset game state function
def reset_game():
    global ball_x, ball_y, coin_x, coin_y, score, start_ticks, game_over, win
    ball_x, ball_y = WIDTH // 2, HEIGHT // 2
    coin_x, coin_y = random.randint(coin_radius, WIDTH - coin_radius), random.randint(coin_radius, HEIGHT - coin_radius)
    score = 0
    start_ticks = pygame.time.get_ticks()
    game_over = False
    win = False

# Initial game state
reset_game()

# Game loop
running = True
clock = pygame.time.Clock()
end_time = None

while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Only update game if it's not over
    if not game_over:
        # Move the ball
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and ball_x - ball_radius > 0:
            ball_x -= ball_speed
        if keys[pygame.K_RIGHT] and ball_x + ball_radius < WIDTH:
            ball_x += ball_speed
        if keys[pygame.K_UP] and ball_y - ball_radius > 0:
            ball_y -= ball_speed
        if keys[pygame.K_DOWN] and ball_y + ball_radius < HEIGHT:
            ball_y += ball_speed

        # Check collision with coin
        distance = ((ball_x - coin_x) ** 2 + (ball_y - coin_y) ** 2) ** 0.5
        if distance < ball_radius + coin_radius:
            score += 1
            coin_x = random.randint(coin_radius, WIDTH - coin_radius)
            coin_y = random.randint(coin_radius, HEIGHT - coin_radius)

        # Check for win condition
        if score >= target_score:
            game_over = True
            win = True
            end_time = pygame.time.get_ticks()

        # Check for lose condition based on time
        seconds = (pygame.time.get_ticks() - start_ticks) / 1000  # Calculate elapsed time
        if seconds > time_limit:
            game_over = True
            win = False
            end_time = pygame.time.get_ticks()

    # Drawing
    screen.fill(WHITE)
    pygame.draw.circle(screen, RED, (ball_x, ball_y), ball_radius)
    pygame.draw.circle(screen, GOLD, (coin_x, coin_y), coin_radius)

    # Display score and timer
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))
    timer_text = font.render(f"Time: {max(0, int(time_limit - seconds))}", True, BLACK)
    screen.blit(timer_text, (WIDTH - 150, 10))

    # Check and display game-over messages
    if game_over:
        if win:
            message = font.render("You Win!", True, BLACK)
        else:
            message = font.render("Game Over!", True, BLACK)
        screen.blit(message, (WIDTH // 2 - 50, HEIGHT // 2))

        # Wait for 3 seconds after game over and then reset
        if pygame.time.get_ticks() - end_time > reset_delay:
            reset_game()

    pygame.display.flip()
    clock.tick(35)

pygame.quit()
