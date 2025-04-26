import pygame
import random
from constants import *
from player_data import player

def get_nutrition_advice():
    advice_list = [
        "Eat colorful veggies for nutrients!",
        "Proteins help muscles recover!",
        "Whole grains give lasting energy!",
        "Stay hydrated for better digestion!",
        f"You're level {player['level']} - keep going!"
    ]

    if player['nutrients']['protein'] < 50:
        advice_list.append("Low protein detected. Add lean meats, beans!")

    if player['nutrients']['vitamins'] < 30:
        advice_list.append("Low vitamin intake. Eat more fruits and vegetables!")

    return random.choice(advice_list)

def draw_advice(screen):
    screen.fill(TEAL)
    title = medium_font.render('Nutrition Advice', True, WHITE)
    screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 50))

    advice = get_nutrition_advice()
    words = advice.split(' ')
    lines = []
    current_line = words[0]

    for word in words[1:]:
        test_line = current_line + ' ' + word
        test_width = small_font.size(test_line)[0]
        if test_width < 500:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word
    lines.append(current_line)

    y = 200
    for line in lines:
        advice_text = tiny_font.render(line, True, WHITE)
        screen.blit(advice_text, (SCREEN_WIDTH//2 - advice_text.get_width()//2, y))
        y += 30

    back_button = pygame.Rect(SCREEN_WIDTH//2 - 100, 400, 200, 50)
    pygame.draw.rect(screen, YELLOW, back_button)
    text = small_font.render('Back', True, BLACK)
    screen.blit(text, (back_button.x + back_button.width//2 - text.get_width()//2,
                       back_button.y + back_button.height//2 - text.get_height()//2))
    return back_button
