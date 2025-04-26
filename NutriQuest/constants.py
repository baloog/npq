import pygame

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
TEAL = (0, 128, 128)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
PURPLE = (128, 0, 128)

# Screen
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600

# Fonts
pygame.font.init()
title_font = pygame.font.Font(None, 74)
medium_font = pygame.font.Font(None, 48)
small_font = pygame.font.Font(None, 36)
tiny_font = pygame.font.Font(None, 24)

# Game states
WELCOME = 0
CREATE_AVATAR = 1
HOME = 2
TRACK_MEAL = 3
MINI_GAME = 4
LEVEL_UP = 5
ADVICE = 6

# Global variable
current_state = WELCOME
