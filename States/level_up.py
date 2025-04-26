import pygame
from constants import *

def draw_level_up(screen):
    screen.fill(TEAL)

    congrats = title_font.render('Level Up!', True, YELLOW)
    screen.blit(congrats, (SCREEN_WIDTH//2 - congrats.get_width()//2, 100))

    # Continue button
    continue_button = pygame.Rect(SCREEN_WIDTH//2 - 100, 480, 200, 50)
    pygame.draw.rect(screen, YELLOW, continue_button)
    text = small_font.render('Continue', True, BLACK)
    screen.blit(text, (continue_button.x + continue_button.width//2 - text.get_width()//2,
                       continue_button.y + continue_button.height//2 - text.get_height()//2))
    return continue_button
