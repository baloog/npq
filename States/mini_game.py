import pygame
import random
import math
from constants import *
from food_database import food_database
from player_data import player, add_xp
from constants import LEVEL_UP, HOME

# Enhanced mini-game variables
mini_game_foods = []
mini_game_score = 0
mini_game_time = 30
mini_game_start_time = 0
game_particles = []
floating_texts = []
power_ups = []
player_basket = {'x': SCREEN_WIDTH // 2, 'width': 120, 'height': 80}
basket_speed = 8
power_up_types = ['time_bonus', 'double_points', 'magnet']
current_power_up = None
power_up_end_time = 0
game_background = None

def initialize_mini_game():
    """Set up the mini-game with initial values"""
    global mini_game_foods, mini_game_score, mini_game_start_time, game_particles
    global floating_texts, power_ups, current_power_up, power_up_end_time, game_background
    
    mini_game_foods = []
    mini_game_score = 0
    mini_game_start_time = pygame.time.get_ticks()
    game_particles = []
    floating_texts = []
    power_ups = []
    current_power_up = None
    power_up_end_time = 0
    
    # Create 5 initial food items
    for _ in range(5):
        spawn_food_item()
    
    # Create a random colorful background pattern
    game_background = create_background_pattern()

def create_background_pattern():
    """Create a colorful background for the game"""
    surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    
    # Fill with base color
    surface.fill(TEAL)
    
    # Add some decorative elements
    for _ in range(20):
        x = random.randint(0, SCREEN_WIDTH)
        y = random.randint(0, SCREEN_HEIGHT)
        radius = random.randint(5, 30)
        color = (random.randint(0, 50), random.randint(150, 255), random.randint(150, 255), 100)
        pygame.draw.circle(surface, color, (x, y), radius)
    
    return surface

def spawn_food_item():
    """Spawn a new food item with random properties"""
    # Choose a random food from the database
    food_name = random.choice(list(food_database.keys()))
    food_data = food_database[food_name]
    
    # Determine if it's healthy or unhealthy
    is_healthy = food_data['calories'] < 200
    
    # Give it random properties
    mini_game_foods.append({
        'name': food_name,
        'x': random.randint(50, SCREEN_WIDTH - 130),
        'y': -80,  # Start above the screen
        'speed': random.uniform(2, 5),
        'rotation': 0,
        'rotation_speed': random.uniform(-2, 2),
        'scale': random.uniform(0.8, 1.2),
        'is_healthy': is_healthy,
        'wobble': random.uniform(0, 3),
        'wobble_speed': random.uniform(0.05, 0.1)
    })

def spawn_power_up():
    """Spawn a new power-up item"""
    if random.random() < 0.2:  # 20% chance to spawn a power-up
        power_up_type = random.choice(power_up_types)
        power_ups.append({
            'type': power_up_type,
            'x': random.randint(50, SCREEN_WIDTH - 130),
            'y': -50,
            'speed': 3,
            'rotation': 0,
            'rotation_speed': 3
        })

def update_mini_game():
    """Update all game elements"""
    global mini_game_foods, game_particles, floating_texts, power_ups, current_power_up, power_up_end_time, mini_game_score
    
    # Update the current time
    current_time = pygame.time.get_ticks()
    
    # Update food items
    for food in mini_game_foods[:]:
        # Apply movement
        food['y'] += food['speed']
        food['rotation'] += food['rotation_speed']
        
        # Apply wobble effect
        food['x'] += math.sin(current_time * food['wobble_speed']) * food['wobble']
        
        # Remove if off-screen
        if food['y'] > SCREEN_HEIGHT:
            mini_game_foods.remove(food)
            
            # Penalty for missing healthy food
            if food['is_healthy']:
                create_floating_text(SCREEN_WIDTH//2, SCREEN_HEIGHT//2, "-5 points!", (255, 50, 50), 36)
                mini_game_score = max(0, mini_game_score - 5)
    
    # Update power-ups
    for power_up in power_ups[:]:
        power_up['y'] += power_up['speed']
        power_up['rotation'] += power_up['rotation_speed']
        
        if power_up['y'] > SCREEN_HEIGHT:
            power_ups.remove(power_up)
    
    # Update particles
    for particle in game_particles[:]:
        particle['life'] -= 1
        particle['x'] += particle['vx']
        particle['y'] += particle['vy']
        particle['size'] -= 0.2
        
        if particle['life'] <= 0 or particle['size'] <= 0:
            game_particles.remove(particle)
    
    # Update floating texts
    for text in floating_texts[:]:
        text['y'] -= text['speed']
        text['life'] -= 1
        
        if text['life'] <= 0:
            floating_texts.remove(text)
    
    # Check for power-up expiration
    if current_power_up and current_time > power_up_end_time:
        current_power_up = None
    
    # Spawn new food items
    time_elapsed = (current_time - mini_game_start_time) // 1000
    
    # Gradually increase difficulty
    if time_elapsed > 0 and time_elapsed % 3 == 0 and len(mini_game_foods) < 6 + time_elapsed // 5:
        spawn_food_item()
    
    # Occasionally spawn power-ups
    if time_elapsed > 0 and time_elapsed % 5 == 0 and random.random() < 0.2:
        spawn_power_up()

def create_particles(x, y, color, count=10):
    """Create particle effects at the given position"""
    for _ in range(count):
        angle = random.uniform(0, math.pi * 2)
        speed = random.uniform(1, 3)
        game_particles.append({
            'x': x,
            'y': y,
            'vx': math.cos(angle) * speed,
            'vy': math.sin(angle) * speed,
            'color': color,
            'size': random.uniform(3, 8),
            'life': random.randint(20, 40)
        })

def create_floating_text(x, y, text, color, size, lifetime=60):
    """Create a floating text element"""
    floating_texts.append({
        'x': x,
        'y': y,
        'text': text,
        'color': color,
        'size': size,
        'speed': 1,
        'life': lifetime
    })

def activate_power_up(power_type):
    """Activate a power-up effect"""
    global current_power_up, power_up_end_time, mini_game_time, mini_game_start_time
    
    current_time = pygame.time.get_ticks()
    current_power_up = power_type
    power_up_end_time = current_time + 5000  # Power-ups last 5 seconds
    
    effect_text = ""
    if power_type == 'time_bonus':
        mini_game_time += 5
        effect_text = "+5 seconds!"
    elif power_type == 'double_points':
        effect_text = "Double points!"
    elif power_type == 'magnet':
        effect_text = "Food magnet!"
    
    create_floating_text(SCREEN_WIDTH//2, SCREEN_HEIGHT//2, effect_text, (255, 215, 0), 40)

def draw_mini_game(screen):
    """Draw all game elements to the screen"""
    # Draw background
    if game_background:
        screen.blit(game_background, (0, 0))
    else:
        screen.fill(TEAL)
    
    # Get time information
    current_time = pygame.time.get_ticks()
    time_left = max(0, mini_game_time - (current_time - mini_game_start_time) // 1000)
    
    # Draw UI elements
    title = medium_font.render('Healthy Food Dash!', True, WHITE)
    screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 20))
    
    # Draw time with a more interesting visual
    time_text = small_font.render(f"Time: {time_left}s", True, WHITE)
    time_bg = pygame.Rect(SCREEN_WIDTH - 220, 20, 200, 40)
    pygame.draw.rect(screen, (0, 100, 130), time_bg, border_radius=10)
    screen.blit(time_text, (SCREEN_WIDTH - 210, 30))
    
    # Draw time bar
    time_ratio = time_left / mini_game_time
    time_bar_bg = pygame.Rect(SCREEN_WIDTH - 220, 65, 200, 15)
    time_bar = pygame.Rect(SCREEN_WIDTH - 220, 65, 200 * time_ratio, 15)
    pygame.draw.rect(screen, (100, 100, 100), time_bar_bg, border_radius=7)
    pygame.draw.rect(screen, (255, 255 * time_ratio, 50), time_bar, border_radius=7)
    
    # Draw score with a fancy background
    score_bg = pygame.Rect(20, 20, 150, 40)
    pygame.draw.rect(screen, (0, 100, 130), score_bg, border_radius=10)
    score_text = small_font.render(f"Score: {mini_game_score}", True, WHITE)
    screen.blit(score_text, (30, 30))
    
    # Draw active power-up indicator
    if current_power_up:
        power_up_bg = pygame.Rect(20, 65, 150, 30)
        pygame.draw.rect(screen, (255, 215, 0), power_up_bg, border_radius=10)
        power_text = small_font.render(current_power_up.replace('_', ' ').title(), True, BLACK)
        screen.blit(power_text, (30, 70))
    
    # Draw player's basket
    basket_rect = pygame.Rect(player_basket['x'] - player_basket['width']//2, 
                              SCREEN_HEIGHT - 100, 
                              player_basket['width'], 
                              player_basket['height'])
    
    # Draw basket shadow for 3D effect
    shadow_rect = basket_rect.copy()
    shadow_rect.y += 5
    pygame.draw.rect(screen, (0, 0, 0, 128), shadow_rect, border_radius=15)
    
    # Draw actual basket
    pygame.draw.rect(screen, YELLOW, basket_rect, border_radius=15)
    
    # Add basket details
    basket_handle = pygame.Rect(basket_rect.centerx - 40, basket_rect.y - 15, 80, 20)
    pygame.draw.ellipse(screen, YELLOW, basket_handle)
    
    # Draw "Catch Healthy Foods!" text
    basket_text = small_font.render("Catch Healthy Foods!", True, BLACK)
    screen.blit(basket_text, (basket_rect.centerx - basket_text.get_width()//2, 
                              basket_rect.centery - basket_text.get_height()//2))
    
    buttons = {}
    # Draw food items with rotation and effects
    for i, food_item in enumerate(mini_game_foods):
        # Create a surface for the food item
        food_size = int(80 * food_item['scale'])
        food_surface = pygame.Surface((food_size, food_size), pygame.SRCALPHA)
        
        # Choose color based on health value
        if food_item['is_healthy']:
            food_color = (0, 200, 0)  # Green for healthy
        else:
            food_color = (200, 0, 0)  # Red for unhealthy
        
        # Draw the food on the surface
        pygame.draw.ellipse(food_surface, food_color, (0, 0, food_size, food_size))
        food_inner = pygame.Rect(food_size//4, food_size//4, food_size//2, food_size//2)
        pygame.draw.ellipse(food_surface, (255, 255, 255, 150), food_inner)
        
        # Create a text surface for the food name
        name_text = small_font.render(food_item['name'].capitalize()[:8], True, WHITE)
        # Center the text on the food
        text_pos = (food_size//2 - name_text.get_width()//2,
                   food_size//2 - name_text.get_height()//2)
        food_surface.blit(name_text, text_pos)
        
        # Rotate the food surface
        rotated_food = pygame.transform.rotate(food_surface, food_item['rotation'])
        
        # Calculate the position with offset due to rotation
        food_rect = rotated_food.get_rect(center=(food_item['x'] + food_size//2, 
                                                  food_item['y'] + food_size//2))
        
        # Draw the rotated food
        screen.blit(rotated_food, food_rect.topleft)
        
        # Store the rect for collision detection
        buttons[f'food_{i}'] = food_rect
    
    # Draw power-ups
    for i, power_up in enumerate(power_ups):
        power_up_surface = pygame.Surface((50, 50), pygame.SRCALPHA)
        
        # Different colors for different power-ups
        if power_up['type'] == 'time_bonus':
            color = (0, 255, 255)  # Cyan for time bonus
            pygame.draw.polygon(power_up_surface, color, [(25, 0), (50, 25), (25, 50), (0, 25)])
        elif power_up['type'] == 'double_points':
            color = (255, 255, 0)  # Yellow for double points
            pygame.draw.circle(power_up_surface, color, (25, 25), 25)
        elif power_up['type'] == 'magnet':
            color = (255, 0, 255)  # Magenta for magnet
            pygame.draw.rect(power_up_surface, color, (5, 5, 40, 40))
        
        # Add a glowing effect
        glow = pygame.Surface((60, 60), pygame.SRCALPHA)
        pygame.draw.circle(glow, (*color[:3], 100), (30, 30), 30)
        screen.blit(glow, (power_up['x'] - 5, power_up['y'] - 5))
        
        # Rotate the power-up
        rotated_power_up = pygame.transform.rotate(power_up_surface, power_up['rotation'])
        power_up_rect = rotated_power_up.get_rect(center=(power_up['x'] + 25, power_up['y'] + 25))
        
        # Draw the rotated power-up
        screen.blit(rotated_power_up, power_up_rect.topleft)
        
        # Store the rect for collision detection
        buttons[f'power_up_{i}'] = power_up_rect
    
    # Draw particles
    for particle in gam
