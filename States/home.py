import pygame
from constants import *
from player_data import player

def draw_home(screen):
    screen.fill(TEAL)
    text = medium_font.render(f"Welcome, {player['name']}!", True, WHITE)
    screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, 30))

    buttons = {}
    # Track Meal, Play Game, Get Advice, Save buttons drawn here
    return buttons

def handle_home_buttons(key):
    from constants import TRACK_MEAL, MINI_GAME, ADVICE
    from constants import current_state

    if key == 'track_meal':
        current_state = TRACK_MEAL
    elif key == 'play_game':
        current_state = MINI_GAME
    elif key == 'advice':
        current_state = ADVICE
    elif key == 'save':
        from save_load import save_game
        save_game()
