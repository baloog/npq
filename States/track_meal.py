import pygame
from constants import *
from player_data import player, add_xp
from food_database import food_database, calculate_nutritional_score
from constants import HOME
from constants import current_state

selected_food = None
show_food_details = False

def draw_track_meal(screen):
    screen.fill(TEAL)
    title = medium_font.render('Track Your Meal', True, WHITE)
    screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 30))

    buttons = {}
    y_offset = 120
    col = 0

    for i, (food_name, food_data) in enumerate(food_database.items()):
        col = i // 6
        row = i % 6
        x_pos = 50 + col * 350
        y_pos = y_offset + row * 60
        food_button = pygame.Rect(x_pos, y_pos, 300, 50)

        button_color = YELLOW if i % 2 == 0 else (220, 220, 0)
        pygame.draw.rect(screen, button_color, food_button)

        food_text = small_font.render(food_name.capitalize(), True, BLACK)
        screen.blit(food_text, (x_pos + 10, y_pos + 10))

        cal_text = tiny_font.render(f"{food_data['calories']} cal", True, BLACK)
        screen.blit(cal_text, (x_pos + 200, y_pos + 10))

        buttons[food_name] = food_button

    back_button = pygame.Rect(20, 20, 80, 40)
    pygame.draw.rect(screen, YELLOW, back_button)
    back_text = tiny_font.render('Back', True, BLACK)
    screen.blit(back_text, (back_button.x + back_button.width//2 - back_text.get_width()//2,
                            back_button.y + back_button.height//2 - back_text.get_height()//2))
    buttons['back'] = back_button

    return buttons, None

def handle_track_meal_buttons(buttons, mouse_click, mouse_pos):
    global selected_food, show_food_details
    for key, btn in buttons.items():
        if btn.collidepoint(mouse_pos) and mouse_click:
            if key == 'back':
                from constants import HOME
                from constants import current_state
                current_state = HOME
            else:
                selected_food = key
                show_food_details = True

    if show_food_details and selected_food:
        draw_meal_details(selected_food)

def draw_meal_details(food):
    pass  # You can modularize it similar to your popup behavior later
