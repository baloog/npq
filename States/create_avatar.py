import pygame
from constants import *
from player_data import player, avatar_colors, avatar_hairstyles, avatar_outfits

def draw_create_avatar(screen):
    screen.fill(TEAL)
    text = medium_font.render('Create Your Avatar', True, WHITE)
    screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, 50))

    name_text = small_font.render(f'Name: {player["name"]}', True, WHITE)
    screen.blit(name_text, (SCREEN_WIDTH//2 - name_text.get_width()//2, 120))

    # Skin color, hairstyle, outfit selections
    buttons = {}
    # ... (same logic drawing buttons)
    return buttons

def handle_avatar_buttons(key):
    if key.startswith('skin_'):
        idx = int(key.split('_')[1])
        player['avatar']['skin_color'] = avatar_colors[idx]
    elif key.startswith('hair_'):
        idx = int(key.split('_')[1])
        player['avatar']['hairstyle'] = avatar_hairstyles[idx]
    elif key.startswith('outfit_'):
        idx = int(key.split('_')[1])
        player['avatar']['outfit'] = avatar_outfits[idx]
    elif key == 'done':
        from constants import HOME
        from constants import current_state
        current_state = HOME
