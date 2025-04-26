import pygame
import sys
import random

# Initialize pygame
pygame.init()

# Screen setup
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('NeuroQuest - Welcome')

# Colors
WHITE = (255, 255, 255)
LIGHT_BLUE = (173, 216, 230)
DEEP_PURPLE = (102, 51, 153)
BLACK = (0, 0, 0)

# Fonts
title_font = pygame.font.Font(None, 74)
button_font = pygame.font.Font(None, 36)

# Particle class for colorful floating magic
class Particle:
    def __init__(self):
        self.x = random.randint(0, SCREEN_WIDTH)
        self.y = random.randint(0, SCREEN_HEIGHT)
        self.size = random.randint(2, 6)
        self.speed_x = random.uniform(-0.5, 0.5)
        self.speed_y = random.uniform(-1.5, -0.5)
        self.color = random.choice([
            (255, 255, 255),  # White
            (255, 182, 193),  # Light Pink
            (173, 216, 230),  # Light Blue
            (144, 238, 144),  # Light Green
            (255, 255, 153),  # Light Yellow
            (221, 160, 221),  # Plum
            (255, 204, 153),  # Light Orange
        ])

    def move(self):
        self.x += self.speed_x
        self.y += self.speed_y
        if self.y < 0:
            self.y = SCREEN_HEIGHT
            self.x = random.randint(0, SCREEN_WIDTH)
            self.color = random.choice([
                (255, 255, 255),
                (255, 182, 193),
                (173, 216, 230),
                (144, 238, 144),
                (255, 255, 153),
                (221, 160, 221),
                (255, 204, 153),
            ])

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.size)

# Create MORE colorful particles
particles = [Particle() for _ in range(200)]  # 200 particles (before it was 100!)

# Main loop
running = True
while running:
    screen.fill(LIGHT_BLUE)

    # Move and draw particles
    for p in particles:
        p.move()
        p.draw(screen)

    # Welcome Text
    title_surface = title_font.render('Welcome, Hero!', True, DEEP_PURPLE)
    title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, 200))
    screen.blit(title_surface, title_rect)

    # Start Button
    start_text = button_font.render('Start Your Quest', True, BLACK)
    start_rect = start_text.get_rect(center=(SCREEN_WIDTH // 2, 400))
    pygame.draw.rect(screen, WHITE, start_rect.inflate(30, 20), border_radius=15)
    screen.blit(start_text, start_rect)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if start_rect.collidepoint(mouse_pos):
                print("Start Button Clicked!")

    pygame.display.flip()

pygame.quit()
sys.exit()
