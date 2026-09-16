import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
FPS = 60

# Colors
YELLOW = (255, 255, 0)
GREEN = (0, 200, 0)
SKY_BLUE = (112, 197, 206)

# Setup Screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird Python")
clock = pygame.time.Clock()

# Game Variables
bird_rect = pygame.Rect(50, 300, 30, 30)
bird_velocity = 0
gravity = 0.25
jump_strength = -6

pipe_width = 50
pipe_gap = 150
pipes = [] # List of [top_rect, bottom_rect]

def create_pipe():
    # Random height for the top pipe
    top_height = random.randint(50, SCREEN_HEIGHT - 150 - pipe_gap)
    top_rect = pygame.Rect(SCREEN_WIDTH, 0, pipe_width, top_height)
    bottom_rect = pygame.Rect(SCREEN_WIDTH, top_height + pipe_gap, pipe_width, SCREEN_HEIGHT)
    return [top_rect, bottom_rect]

# Main Game Loop
while True:
    # 1. Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE: # Press Space to jump
                bird_velocity = jump_strength

    # 2. Physics & Logic
    bird_velocity += gravity
    bird_rect.y += int(bird_velocity)

    # Pipe movement
    if not pipes or pipes[-1][0].x < SCREEN_WIDTH - 250:
        pipes.append(create_pipe())

    for pipe in pipes:
        pipe[0].x -= 2
        pipe[1].x -= 2

    # Collision & Cleanup
    # Check boundaries
    if bird_rect.y > SCREEN_HEIGHT or bird_rect.y < 0:
        bird_rect.y = 300
        bird_velocity = 0
        pipes = []
    
    # Check pipe collisions
    for pipe in pipes:
        if bird_rect.colliderect(pipe[0]) or bird_rect.colliderect(pipe[1]):
            bird_rect.y = 300
            bird_velocity = 0
            pipes = []

    # Remove off-screen pipes
    pipes = [p for p in pipes if p[0].x > -pipe_width]

    # 3. Drawing
    screen.fill(SKY_BLUE)
    pygame.draw.rect(screen, YELLOW, bird_rect)
    for pipe in pipes:
        pygame.draw.rect(screen, GREEN, pipe[0])
        pygame.draw.rect(screen, GREEN, pipe[1])

    pygame.display.flip()
    clock.tick(FPS)
