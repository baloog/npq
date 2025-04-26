import pygame
import sys
import json
import random
import os
import requests
from datetime import datetime

# Initialize pygame
pygame.init()

# Screen setup
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('NutriQuest')

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
TEAL = (0, 128, 128)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
PURPLE = (128, 0, 128)

# Fonts
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

# Current game state
current_state = WELCOME

# Avatar variables
avatar_colors = [(255, 200, 150), (200, 150, 100), (150, 100, 50)]
avatar_hairstyles = ['short', 'medium', 'long']
avatar_outfits = ['casual', 'sporty', 'formal']

# Player data
player = {
    'name': '',
    'avatar': {
        'skin_color': avatar_colors[0],
        'hairstyle': avatar_hairstyles[0],
        'outfit': avatar_outfits[0]
    },
    'level': 1,
    'xp': 0,
    'meals': [],
    'nutrients': {
        'calories': 0,
        'protein': 0,
        'carbs': 0,
        'fat': 0,
        'vitamins': 0
    },
    'high_score': 0,
    'daily_streak': 0,
    'last_played': None
}

# Food database - we'll use a simplified version, but in production we'd use an API
food_database = {
    'apple': {'calories': 95, 'protein': 0.5, 'carbs': 25, 'fat': 0.3, 'vitamins': 8, 'image': 'apple'},
    'banana': {'calories': 105, 'protein': 1.3, 'carbs': 27, 'fat': 0.4, 'vitamins': 9, 'image': 'banana'},
    'broccoli': {'calories': 55, 'protein': 3.7, 'carbs': 11, 'fat': 0.6, 'vitamins': 15, 'image': 'broccoli'},
    'chicken': {'calories': 165, 'protein': 31, 'carbs': 0, 'fat': 3.6, 'vitamins': 5, 'image': 'chicken'},
    'salmon': {'calories': 208, 'protein': 20, 'carbs': 0, 'fat': 13, 'vitamins': 11, 'image': 'salmon'},
    'rice': {'calories': 130, 'protein': 2.7, 'carbs': 28, 'fat': 0.3, 'vitamins': 2, 'image': 'rice'},
    'pizza': {'calories': 285, 'protein': 12, 'carbs': 36, 'fat': 10, 'vitamins': 4, 'image': 'pizza'},
    'soda': {'calories': 140, 'protein': 0, 'carbs': 39, 'fat': 0, 'vitamins': 0, 'image': 'soda'},
    'chocolate': {'calories': 210, 'protein': 2, 'carbs': 24, 'fat': 13, 'vitamins': 1, 'image': 'chocolate'},
    'salad': {'calories': 45, 'protein': 1.5, 'carbs': 8, 'fat': 0.5, 'vitamins': 12, 'image': 'salad'},
    'nuts': {'calories': 170, 'protein': 6, 'carbs': 5, 'fat': 14, 'vitamins': 7, 'image': 'nuts'},
    'yogurt': {'calories': 120, 'protein': 10, 'carbs': 8, 'fat': 4, 'vitamins': 8, 'image': 'yogurt'}
}

# Mini-game variables
mini_game_foods = []
mini_game_score = 0
mini_game_time = 30
mini_game_start_time = 0


# Function to fetch nutrition data from an API (simulation)
def fetch_food_data(food_name):
    # In production, this would call an API like Nutritionix or USDA Food Database
    if food_name.lower() in food_database:
        return food_database[food_name.lower()]
    else:
        # Return default values
        return {'calories': 100, 'protein': 2, 'carbs': 15, 'fat': 5, 'vitamins': 3, 'image': 'default'}


# Save and load functions
def save_game():
    player['last_played'] = datetime.now().strftime("%Y-%m-%d")
    with open('nutriquest_save.json', 'w') as f:
        json.dump(player, f)


def load_game():
    global player
    try:
        with open('nutriquest_save.json', 'r') as f:
            player = json.load(f)
    except FileNotFoundError:
        pass  # Use default player data


# XP and leveling system
def add_xp(amount):
    player['xp'] += amount
    # Level up if XP reaches threshold
    level_threshold = player['level'] * 100
    if player['xp'] >= level_threshold:
        player['level'] += 1
        player['xp'] -= level_threshold
        return True  # Indicates a level up
    return False


def calculate_nutritional_score(food):
    # Simple scoring system based on nutritional balance
    score = 0
    score += food['protein'] * 3  # Protein is valuable
    score += food['vitamins'] * 4  # Vitamins are very valuable
    score -= food['fat'] * 1  # Fat reduces score slightly

    # Carbs are neutral but too many reduce score
    if food['carbs'] > 30:
        score -= (food['carbs'] - 30) / 2

    return max(5, score)  # Minimum 5 points for any food


def get_nutrition_advice():
    advice_list = [
        "Try to eat a rainbow of colors for a wide range of nutrients!",
        "Protein helps build and repair muscles after exercise.",
        "Whole grains provide long-lasting energy throughout the day.",
        "Drinking water helps maintain energy levels and aids digestion.",
        "Fruits and vegetables provide essential vitamins and minerals.",
        "Limit sugary drinks and snacks to maintain stable energy levels.",
        "Breakfast kickstarts your metabolism for the day!",
        "Small, frequent meals can help maintain energy and metabolism.",
        f"You've tracked {len(player['meals'])} meals - keep up the good work!",
        f"You're level {player['level']} - eating balanced meals helps you level up faster!"
    ]

    # Personalized advice based on player data
    if player['nutrients']['protein'] < 50:
        advice_list.append("Your protein intake seems low. Try adding more lean meats, beans, or nuts to your diet.")

    if player['nutrients']['vitamins'] < 30:
        advice_list.append("Your vitamin intake could be improved. Try adding more colorful fruits and vegetables!")

    if player['nutrients']['calories'] > 2500:
        advice_list.append("You're consuming quite a few calories. Balance with exercise and nutrient-dense foods.")

    return random.choice(advice_list)


# Drawing avatar
def draw_avatar(x, y, size):
    # Draw body
    pygame.draw.circle(screen, player['avatar']['skin_color'], (x, y - size // 2), size // 3)  # Head
    pygame.draw.rect(screen, player['avatar']['skin_color'],
                     (x - size // 4, y - size // 4, size // 2, size // 2))  # Body

    # Draw hairstyle
    if player['avatar']['hairstyle'] == 'short':
        pygame.draw.rect(screen, BLACK, (x - size // 4, y - size // 2 - size // 10, size // 2, size // 10))
    elif player['avatar']['hairstyle'] == 'medium':
        pygame.draw.rect(screen, BLACK, (x - size // 3, y - size // 2 - size // 8, size // 1.5, size // 8))
    else:  # long
        pygame.draw.rect(screen, BLACK, (x - size // 3, y - size // 2 - size // 6, size // 1.5, size // 6))

    # Draw outfit
    outfit_color = BLUE if player['avatar']['outfit'] == 'casual' else \
        GREEN if player['avatar']['outfit'] == 'sporty' else PURPLE
    pygame.draw.rect(screen, outfit_color, (x - size // 4, y - size // 4, size // 2, size // 2))  # Clothes


# Drawing functions for each game state
def draw_welcome():
    screen.fill(TEAL)

    # Title
    text = title_font.render('Welcome to NutriQuest!', True, WHITE)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 150))

    # Start button
    start_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, 400, 200, 50)
    pygame.draw.rect(screen, YELLOW, start_button)
    button_text = small_font.render('Start Quest', True, BLACK)
    screen.blit(button_text, (start_button.x + start_button.width // 2 - button_text.get_width() // 2,
                              start_button.y + start_button.height // 2 - button_text.get_height() // 2))

    return start_button


def draw_create_avatar():
    screen.fill(TEAL)

    # Title
    text = medium_font.render('Create Your Avatar', True, WHITE)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 50))

    # Name input
    name_text = small_font.render(f'Name: {player["name"]}', True, WHITE)
    screen.blit(name_text, (SCREEN_WIDTH // 2 - name_text.get_width() // 2, 120))

    # Avatar preview
    draw_avatar(SCREEN_WIDTH // 2, 250, 100)

    # Selection buttons
    buttons = {}

    # Skin color options
    text = small_font.render('Skin Tone:', True, WHITE)
    screen.blit(text, (150, 350))
    for i, color in enumerate(avatar_colors):
        button = pygame.Rect(150 + i * 40, 380, 30, 30)
        pygame.draw.rect(screen, color, button)
        if color == player['avatar']['skin_color']:
            pygame.draw.rect(screen, WHITE, button, 2)  # Highlight selected
        buttons[f'skin_{i}'] = button

    # Hairstyle options
    text = small_font.render('Hairstyle:', True, WHITE)
    screen.blit(text, (350, 350))
    for i, style in enumerate(avatar_hairstyles):
        button = pygame.Rect(350 + i * 75, 380, 65, 30)
        pygame.draw.rect(screen, WHITE, button)
        style_text = tiny_font.render(style, True, BLACK)
        screen.blit(style_text, (button.x + button.width // 2 - style_text.get_width() // 2,
                                 button.y + button.height // 2 - style_text.get_height() // 2))
        if style == player['avatar']['hairstyle']:
            pygame.draw.rect(screen, YELLOW, button, 2)  # Highlight selected
        buttons[f'hair_{i}'] = button

    # Outfit options
    text = small_font.render('Outfit:', True, WHITE)
    screen.blit(text, (150, 450))
    for i, outfit in enumerate(avatar_outfits):
        button = pygame.Rect(150 + i * 75, 480, 65, 30)
        outfit_color = BLUE if outfit == 'casual' else \
            GREEN if outfit == 'sporty' else PURPLE
        pygame.draw.rect(screen, outfit_color, button)
        outfit_text = tiny_font.render(outfit, True, WHITE)
        screen.blit(outfit_text, (button.x + button.width // 2 - outfit_text.get_width() // 2,
                                  button.y + button.height // 2 - outfit_text.get_height() // 2))
        if outfit == player['avatar']['outfit']:
            pygame.draw.rect(screen, YELLOW, button, 2)  # Highlight selected
        buttons[f'outfit_{i}'] = button

    # Done button
    done_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, 530, 200, 50)
    pygame.draw.rect(screen, YELLOW, done_button)
    button_text = small_font.render('Done', True, BLACK)
    screen.blit(button_text, (done_button.x + done_button.width // 2 - button_text.get_width() // 2,
                              done_button.y + done_button.height // 2 - button_text.get_height() // 2))
    buttons['done'] = done_button

    return buttons


def draw_home():
    screen.fill(TEAL)

    # Title and stats
    text = medium_font.render(f"Welcome, {player['name']}!", True, WHITE)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 30))

    level_text = small_font.render(f"Level: {player['level']}   XP: {player['xp']}/{player['level'] * 100}", True,
                                   WHITE)
    screen.blit(level_text, (SCREEN_WIDTH // 2 - level_text.get_width() // 2, 80))

    # Draw avatar
    draw_avatar(SCREEN_WIDTH // 2, 180, 120)

    # Nutrition summary
    summary_text = small_font.render("Nutrition Summary:", True, WHITE)
    screen.blit(summary_text, (50, 250))

    nutrients = player['nutrients']
    cal_text = tiny_font.render(f"Calories: {nutrients['calories']}", True, WHITE)
    screen.blit(cal_text, (50, 290))

    protein_text = tiny_font.render(f"Protein: {nutrients['protein']}g", True, WHITE)
    screen.blit(protein_text, (50, 320))

    carbs_text = tiny_font.render(f"Carbs: {nutrients['carbs']}g", True, WHITE)
    screen.blit(carbs_text, (50, 350))

    fat_text = tiny_font.render(f"Fat: {nutrients['fat']}g", True, WHITE)
    screen.blit(fat_text, (50, 380))

    vitamins_text = tiny_font.render(f"Vitamin Score: {nutrients['vitamins']}", True, WHITE)
    screen.blit(vitamins_text, (50, 410))

    # Menu options
    buttons = {}

    track_meal_button = pygame.Rect(SCREEN_WIDTH // 2 - 200, 300, 180, 50)
    pygame.draw.rect(screen, YELLOW, track_meal_button)
    button_text = small_font.render('Track Meal', True, BLACK)
    screen.blit(button_text, (track_meal_button.x + track_meal_button.width // 2 - button_text.get_width() // 2,
                              track_meal_button.y + track_meal_button.height // 2 - button_text.get_height() // 2))
    buttons['track_meal'] = track_meal_button

    play_game_button = pygame.Rect(SCREEN_WIDTH // 2 + 20, 300, 180, 50)
    pygame.draw.rect(screen, YELLOW, play_game_button)
    button_text = small_font.render('Play Game', True, BLACK)
    screen.blit(button_text, (play_game_button.x + play_game_button.width // 2 - button_text.get_width() // 2,
                              play_game_button.y + play_game_button.height // 2 - button_text.get_height() // 2))
    buttons['play_game'] = play_game_button

    advice_button = pygame.Rect(SCREEN_WIDTH // 2 - 200, 380, 180, 50)
    pygame.draw.rect(screen, YELLOW, advice_button)
    button_text = small_font.render('Get Advice', True, BLACK)
    screen.blit(button_text, (advice_button.x + advice_button.width // 2 - button_text.get_width() // 2,
                              advice_button.y + advice_button.height // 2 - button_text.get_height() // 2))
    buttons['advice'] = advice_button

    save_button = pygame.Rect(SCREEN_WIDTH // 2 + 20, 380, 180, 50)
    pygame.draw.rect(screen, YELLOW, save_button)
    button_text = small_font.render('Save Progress', True, BLACK)
    screen.blit(button_text, (save_button.x + save_button.width // 2 - button_text.get_width() // 2,
                              save_button.y + save_button.height // 2 - button_text.get_height() // 2))
    buttons['save'] = save_button

    # High score
    if player['high_score'] > 0:
        score_text = small_font.render(f"Mini-Game High Score: {player['high_score']}", True, WHITE)
        screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 460))

    # Daily streak
    streak_text = small_font.render(f"Daily Streak: {player['daily_streak']} days", True, WHITE)
    screen.blit(streak_text, (SCREEN_WIDTH // 2 - streak_text.get_width() // 2, 500))

    return buttons


def draw_track_meal():
    screen.fill(TEAL)

    # Title
    text = medium_font.render('Track Your Meal', True, WHITE)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 30))

    # Food list
    list_title = small_font.render('Available Foods:', True, WHITE)
    screen.blit(list_title, (50, 80))

    buttons = {}
    y_offset = 120
    col = 0

    # Create two columns of food
    for i, (food_name, food_data) in enumerate(food_database.items()):
        col = i // 6  # 6 items per column
        row = i % 6
        x_pos = 50 + col * 350
        y_pos = y_offset + row * 60

        food_button = pygame.Rect(x_pos, y_pos, 300, 50)

        # Alternate colors for better visibility
        button_color = YELLOW if i % 2 == 0 else (220, 220, 0)
        pygame.draw.rect(screen, button_color, food_button)

        # Food name and basic info
        food_text = small_font.render(food_name.capitalize(), True, BLACK)
        screen.blit(food_text, (x_pos + 10, y_pos + 10))

        cal_text = tiny_font.render(f"{food_data['calories']} cal", True, BLACK)
        screen.blit(cal_text, (x_pos + 200, y_pos + 10))

        # Add to buttons dictionary
        buttons[food_name] = food_button

    # Cooking pot (meal area)
    pot_title = small_font.render('Your Meal:', True, WHITE)
    screen.blit(pot_title, (SCREEN_WIDTH // 2 - pot_title.get_width() // 2, 480))

    pot_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, 520, 200, 60)
    pygame.draw.ellipse(screen, (100, 100, 100), pot_rect)

    # Back button
    back_button = pygame.Rect(20, 20, 80, 40)
    pygame.draw.rect(screen, YELLOW, back_button)
    back_text = tiny_font.render('Back', True, BLACK)
    screen.blit(back_text, (back_button.x + back_button.width // 2 - back_text.get_width() // 2,
                            back_button.y + back_button.height // 2 - back_text.get_height() // 2))
    buttons['back'] = back_button

    return buttons, pot_rect


def draw_meal_details(selected_food):
    # Overlay for meal details after selection
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))  # Semi-transparent background
    screen.blit(overlay, (0, 0))

    # Details window
    details_rect = pygame.Rect(SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 - 150, 400, 300)
    pygame.draw.rect(screen, TEAL, details_rect)
    pygame.draw.rect(screen, WHITE, details_rect, 2)

    # Food name
    food_title = medium_font.render(selected_food.capitalize(), True, WHITE)
    screen.blit(food_title, (SCREEN_WIDTH // 2 - food_title.get_width() // 2, details_rect.y + 20))

    # Nutrition details
    food_data = food_database[selected_food]
    y_offset = details_rect.y + 80

    for nutrient, value in food_data.items():
        if nutrient != 'image':  # Skip the image key
            info_text = small_font.render(f"{nutrient.capitalize()}: {value}", True, WHITE)
            screen.blit(info_text, (details_rect.x + 50, y_offset))
            y_offset += 30

    # XP gain
    xp_gain = int(calculate_nutritional_score(food_data))
    xp_text = small_font.render(f"XP Gain: +{xp_gain}", True, GREEN)
    screen.blit(xp_text, (details_rect.x + 50, y_offset + 10))

    # Buttons
    buttons = {}

    add_button = pygame.Rect(details_rect.x + 50, details_rect.y + 240, 120, 40)
    pygame.draw.rect(screen, GREEN, add_button)
    add_text = small_font.render('Add', True, BLACK)
    screen.blit(add_text, (add_button.x + add_button.width // 2 - add_text.get_width() // 2,
                           add_button.y + add_button.height // 2 - add_text.get_height() // 2))
    buttons['add'] = add_button

    cancel_button = pygame.Rect(details_rect.x + 230, details_rect.y + 240, 120, 40)
    pygame.draw.rect(screen, RED, cancel_button)
    cancel_text = small_font.render('Cancel', True, BLACK)
    screen.blit(cancel_text, (cancel_button.x + cancel_button.width // 2 - cancel_text.get_width() // 2,
                              cancel_button.y + cancel_button.height // 2 - cancel_text.get_height() // 2))
    buttons['cancel'] = cancel_button

    return buttons, xp_gain, food_data


def draw_mini_game():
    screen.fill(TEAL)

    # Title
    text = medium_font.render('Healthy Food Dash!', True, WHITE)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 30))

    # Timer
    time_left = max(0, mini_game_time - (pygame.time.get_ticks() - mini_game_start_time) // 1000)
    time_text = small_font.render(f"Time: {time_left} seconds", True, WHITE)
    screen.blit(time_text, (SCREEN_WIDTH - 200, 30))

    # Score
    score_text = small_font.render(f"Score: {mini_game_score}", True, WHITE)
    screen.blit(score_text, (50, 30))

    # Instructions
    if time_left == mini_game_time:  # Game just started
        instructions = small_font.render("Click on healthy foods quickly! Avoid junk food!", True, WHITE)
        screen.blit(instructions, (SCREEN_WIDTH // 2 - instructions.get_width() // 2, 80))

    # Draw food items
    buttons = {}
    for i, food_item in enumerate(mini_game_foods):
        food_rect = pygame.Rect(food_item['x'], food_item['y'], 80, 80)
        pygame.draw.rect(screen, YELLOW, food_rect)
        food_text = small_font.render(food_item['name'].capitalize(), True, BLACK)
        screen.blit(food_text, (food_item['x'] + 40 - food_text.get_width() // 2,
                                food_item['y'] + 40 - food_text.get_height() // 2))
        buttons[f"food_{i}"] = food_rect

    # Game over check
    if time_left <= 0:
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))

        game_over_text = title_font.render("Time's Up!", True, WHITE)
        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - 80))

        final_score_text = medium_font.render(f"Final Score: {mini_game_score}", True, WHITE)
        screen.blit(final_score_text, (SCREEN_WIDTH // 2 - final_score_text.get_width() // 2, SCREEN_HEIGHT // 2))

        # Update high score if needed
        if mini_game_score > player['high_score']:
            player['high_score'] = mini_game_score
            high_score_text = small_font.render("New High Score!", True, YELLOW)
            screen.blit(high_score_text,
                        (SCREEN_WIDTH // 2 - high_score_text.get_width() // 2, SCREEN_HEIGHT // 2 + 50))

        # XP gained
        xp_gained = mini_game_score // 2
        xp_text = small_font.render(f"XP Gained: +{xp_gained}", True, GREEN)
        screen.blit(xp_text, (SCREEN_WIDTH // 2 - xp_text.get_width() // 2, SCREEN_HEIGHT // 2 + 90))

        # Continue button
        continue_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 130, 200, 50)
        pygame.draw.rect(screen, YELLOW, continue_button)
        continue_text = small_font.render('Continue', True, BLACK)
        screen.blit(continue_text, (continue_button.x + continue_button.width // 2 - continue_text.get_width() // 2,
                                    continue_button.y + continue_button.height // 2 - continue_text.get_height() // 2))
        buttons['continue'] = continue_button

    return buttons


def draw_level_up():
    screen.fill(TEAL)

    # Level up animation/screen
    congrats_text = title_font.render('Level Up!', True, YELLOW)
    screen.blit(congrats_text, (SCREEN_WIDTH // 2 - congrats_text.get_width() // 2, 100))

    level_text = medium_font.render(f"You are now level {player['level']}!", True, WHITE)
    screen.blit(level_text, (SCREEN_WIDTH // 2 - level_text.get_width() // 2, 200))

    # Draw avatar
    draw_avatar(SCREEN_WIDTH // 2, 300, 150)

    # Benefits text
    benefits_text = small_font.render("New nutrition insights unlocked!", True, WHITE)
    screen.blit(benefits_text, (SCREEN_WIDTH // 2 - benefits_text.get_width() // 2, 400))

    # Continue button
    continue_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, 480, 200, 50)
    pygame.draw.rect(screen, YELLOW, continue_button)
    continue_text = small_font.render('Continue', True, BLACK)
    screen.blit(continue_text, (continue_button.x + continue_button.width // 2 - continue_text.get_width() // 2,
                                continue_button.y + continue_button.height // 2 - continue_text.get_height() // 2))

    return continue_button


def draw_advice():
    screen.fill(TEAL)

    # Title
    text = medium_font.render('Nutrition Advice', True, WHITE)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 50))

    # Get advice
    advice = get_nutrition_advice()

    # Advice box
    advice_rect = pygame.Rect(100, 150, SCREEN_WIDTH - 200, 200)
    pygame.draw.rect(screen, (0, 100, 100), advice_rect)
    pygame.draw.rect(screen, WHITE, advice_rect, 2)

    # Render advice text with word wrapping
    words = advice.split(' ')
    lines = []
    current_line = words[0]

    for word in words[1:]:
        test_line = current_line + ' ' + word
        test_width = small_font.size(test_line)[0]
        if test_width < advice_rect.width - 20:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word
    lines.append(current_line)

    y_offset = advice_rect.y + 20
    for line in lines:
        advice_text = tiny_font.render(line, True, WHITE)
        screen.blit(advice_text, (advice_rect.x + 10, y_offset))
        y_offset += 30

    # Back button
    back_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, 400, 200, 50)
    pygame.draw.rect(screen, YELLOW, back_button)
    button_text = small_font.render('Back', True, BLACK)
    screen.blit(button_text, (back_button.x + back_button.width // 2 - button_text.get_width() // 2,
                              back_button.y + back_button.height // 2 - button_text.get_height() // 2))

    return back_button


# ================= Main Game Loop =================

def main():
    global current_state, mini_game_foods, mini_game_score, mini_game_start_time

    clock = pygame.time.Clock()
    running = True
    selected_food = None
    show_food_details = False
    food_buttons = {}
    pot_rect = None
    meal_selected = []

    load_game()

    while running:
        screen.fill(TEAL)

        mouse_pos = pygame.mouse.get_pos()
        mouse_click = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_game()
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_click = True
            if event.type == pygame.KEYDOWN:
                if current_state == CREATE_AVATAR:
                    if event.key == pygame.K_BACKSPACE:
                        player['name'] = player['name'][:-1]
                    else:
                        player['name'] += event.unicode

        if current_state == WELCOME:
            start_button = draw_welcome()
            if start_button.collidepoint(mouse_pos) and mouse_click:
                current_state = CREATE_AVATAR

        elif current_state == CREATE_AVATAR:
            buttons = draw_create_avatar()
            for key, btn in buttons.items():
                if btn.collidepoint(mouse_pos) and mouse_click:
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
                        current_state = HOME

        elif current_state == HOME:
            buttons = draw_home()
            for key, btn in buttons.items():
                if btn.collidepoint(mouse_pos) and mouse_click:
                    if key == 'track_meal':
                        current_state = TRACK_MEAL
                    elif key == 'play_game':
                        mini_game_foods = []
                        for _ in range(5):
                            food_name = random.choice(list(food_database.keys()))
                            mini_game_foods.append({'name': food_name,
                                                    'x': random.randint(50, SCREEN_WIDTH - 130),
                                                    'y': random.randint(100, SCREEN_HEIGHT - 180)})
                        mini_game_score = 0
                        mini_game_start_time = pygame.time.get_ticks()
                        current_state = MINI_GAME
                    elif key == 'advice':
                        current_state = ADVICE
                    elif key == 'save':
                        save_game()

        elif current_state == TRACK_MEAL:
            food_buttons, pot_rect = draw_track_meal()
            for key, btn in food_buttons.items():
                if btn.collidepoint(mouse_pos) and mouse_click:
                    if key == 'back':
                        current_state = HOME
                    else:
                        selected_food = key
                        show_food_details = True

            if show_food_details and selected_food:
                buttons, xp_gain, food_data = draw_meal_details(selected_food)
                for key, btn in buttons.items():
                    if btn.collidepoint(mouse_pos) and mouse_click:
                        if key == 'add':
                            # Add food nutrients to player
                            for nutrient in ['calories', 'protein', 'carbs', 'fat', 'vitamins']:
                                player['nutrients'][nutrient] += food_data[nutrient]
                            player['meals'].append(selected_food)
                            level_up = add_xp(xp_gain)
                            if level_up:
                                current_state = LEVEL_UP
                            else:
                                current_state = TRACK_MEAL
                            show_food_details = False
                            selected_food = None
                        elif key == 'cancel':
                            show_food_details = False
                            selected_food = None

        elif current_state == MINI_GAME:
            buttons = draw_mini_game()
            for key, btn in buttons.items():
                if 'food_' in key and btn.collidepoint(mouse_pos) and mouse_click:
                    idx = int(key.split('_')[1])
                    food_item = mini_game_foods[idx]
                    food_data = food_database[food_item['name']]
                    if food_data['calories'] < 200:  # Assume healthy foods are <200 calories
                        mini_game_score += 10
                    else:
                        mini_game_score -= 5
                    mini_game_foods.pop(idx)

            if 'continue' in buttons and buttons['continue'].collidepoint(mouse_pos) and mouse_click:
                xp_gained = mini_game_score // 2
                level_up = add_xp(xp_gained)
                if level_up:
                    current_state = LEVEL_UP
                else:
                    current_state = HOME

        elif current_state == LEVEL_UP:
            continue_button = draw_level_up()
            if continue_button.collidepoint(mouse_pos) and mouse_click:
                current_state = HOME

        elif current_state == ADVICE:
            back_button = draw_advice()
            if back_button.collidepoint(mouse_pos) and mouse_click:
                current_state = HOME

        pygame.display.update()
        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
