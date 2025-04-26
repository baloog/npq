import pygame
import sys
from constants import *
from player_data import player, add_xp, draw_avatar
from food_database import food_database
from save_load import save_game, load_game
from states import welcome, create_avatar, home, track_meal, mini_game, level_up, advice

def main():
    # 🧙‍♂️ The Magical Journey Begins Here! 🧙‍♂️
    global current_state
    
    # ✨ Summon the mystical pygame powers! ✨
    pygame.init()
    
    # ⏰ The Timekeeper of Our Adventure ⏰
    clock = pygame.time.Clock()
    
    # 🏞️ Create the enchanted window to our nutritional realm 🏞️
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('NutriQuest')
    
    # 📜 Recover the ancient scrolls of player progress 📜
    load_game()
    
    # 🚪 Begin at the gates of our kingdom 🚪
    current_state = WELCOME
    
    # 🔄 The Great Wheel of Game Time Spins Eternally 🔄
    running = True
    while running:
        # 🎨 Paint our magical teal backdrop 🎨
        screen.fill(TEAL)
        
        # 🐭 Track the mystical pointer device 🐭
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = False
        
        # 🎮 Listen for signals from the mortal realm 🎮
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # 💾 Preserve our hero's journey before departure 💾
                save_game()
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_click = True
            if event.type == pygame.KEYDOWN and current_state == CREATE_AVATAR:
                if event.key == pygame.K_BACKSPACE:
                    # ✂️ Trim the hero's name with magical scissors ✂️
                    player['name'] = player['name'][:-1]
                else:
                    # ✍️ Inscribe the hero's legend one rune at a time ✍️
                    player['name'] += event.unicode
        
        # 🔀 The Mystical State Machine of Destiny 🔀
        if current_state == WELCOME:
            # 👋 Greet travelers at the kingdom gates 👋
            start_button = welcome.draw_welcome(screen)
            if start_button.collidepoint(mouse_pos) and mouse_click:
                current_state = CREATE_AVATAR
                
        elif current_state == CREATE_AVATAR:
            # 🧝 Craft your nutritional champion 🧝
            buttons = create_avatar.draw_create_avatar(screen)
            for key, btn in buttons.items():
                if btn.collidepoint(mouse_pos) and mouse_click:
                    create_avatar.handle_avatar_buttons(key)
                    
        elif current_state == HOME:
            # 🏠 The cozy hub of nutritional adventures 🏠
            buttons = home.draw_home(screen)
            for key, btn in buttons.items():
                if btn.collidepoint(mouse_pos) and mouse_click:
                    home.handle_home_buttons(key)
                    
        elif current_state == TRACK_MEAL:
            # 🍽️ The grand feast hall of food tracking 🍽️
            food_buttons, pot_rect = track_meal.draw_track_meal(screen)
            track_meal.handle_track_meal_buttons(food_buttons, mouse_click, mouse_pos)
            
        elif current_state == MINI_GAME:
            # 🎮 The arena of nutritional prowess 🎮
            buttons = mini_game.draw_mini_game(screen)
            mini_game.handle_mini_game_buttons(buttons, mouse_click, mouse_pos)
            
        elif current_state == LEVEL_UP:
            # 🌟 Celebrate the growth of our hero! 🌟
            continue_button = level_up.draw_level_up(screen)
            if continue_button.collidepoint(mouse_pos) and mouse_click:
                current_state = HOME
                
        elif current_state == ADVICE:
            # 🧠 The wise oracle of nutritional wisdom 🧠
            back_button = advice.draw_advice(screen)
            if back_button.collidepoint(mouse_pos) and mouse_click:
                current_state = HOME
        
        # 🔄 Refresh our magical window to the nutritional realm 🔄
        pygame.display.update()
        
        # ⏱️ Control the flow of magical time ⏱️
        clock.tick(60)
    
    # 👋 Bid farewell to our mystical pygame powers 👋
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    # 🚀 Launch our nutritional adventure! 🚀
    main()
