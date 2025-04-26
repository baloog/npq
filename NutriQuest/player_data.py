# Define avatar customization options with more variety and structure
AVATAR_OPTIONS = {
    'skin_colors': {
        'fair': (255, 220, 178),
        'light': (234, 192, 134),
        'medium': (198, 134, 66),
        'dark': (141, 85, 36),
        'deep': (83, 53, 10)
    },
    'hairstyles': {
        'short': {'length': 1, 'styles': ['buzz', 'pixie', 'crew']},
        'medium': {'length': 2, 'styles': ['bob', 'layered', 'wavy']},
        'long': {'length': 3, 'styles': ['straight', 'curly', 'braided']}
    },
    'outfits': {
        'casual': ['tshirt_jeans', 'hoodie', 'sweater'],
        'sporty': ['tracksuit', 'jersey', 'athletic_wear'],
        'formal': ['suit', 'dress', 'business_casual'],
        'fantasy': ['wizard', 'knight', 'ranger']
    },
    'accessories': ['glasses', 'hat', 'necklace', 'earrings', 'none']
}

# Player structure with improved avatar customization
player = {
    'name': '',
    'avatar': {
        'skin_color': 'medium',  # Key from skin_colors dict
        'hairstyle': 'short',    # Key from hairstyles dict
        'hair_style_variant': 'buzz', # Specific style from hairstyles
        'hair_color': (50, 50, 50),   # RGB color tuple
        'outfit': 'casual',      # Key from outfits dict
        'outfit_variant': 'tshirt_jeans', # Specific outfit
        'accessories': []        # List of accessories
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

def add_xp(amount):
    """Add experience points to player and handle level up"""
    level_threshold = player['level'] * 100
    player['xp'] += amount
    level_up = False
    
    # Handle multiple level ups in one go
    while player['xp'] >= level_threshold:
        player['level'] += 1
        player['xp'] -= level_threshold
        level_threshold = player['level'] * 100
        level_up = True
    
    return level_up

def customize_avatar(skin_color=None, hairstyle=None, hair_variant=None, 
                    hair_color=None, outfit=None, outfit_variant=None, 
                    accessories=None):
    """Update avatar with selected customization options"""
    avatar = player['avatar']
    
    # Update skin color if provided and valid
    if skin_color and skin_color in AVATAR_OPTIONS['skin_colors']:
        avatar['skin_color'] = skin_color
    
    # Update hairstyle if provided and valid
    if hairstyle and hairstyle in AVATAR_OPTIONS['hairstyles']:
        avatar['hairstyle'] = hairstyle
        # Reset hair variant if changing hairstyle
        avatar['hair_style_variant'] = AVATAR_OPTIONS['hairstyles'][hairstyle]['styles'][0]
    
    # Update hair style variant if provided and valid
    if hair_variant:
        if hair_variant in AVATAR_OPTIONS['hairstyles'][avatar['hairstyle']]['styles']:
            avatar['hair_style_variant'] = hair_variant
    
    # Update hair color if provided
    if hair_color and isinstance(hair_color, tuple) and len(hair_color) == 3:
        avatar['hair_color'] = hair_color
    
    # Update outfit if provided and valid
    if outfit and outfit in AVATAR_OPTIONS['outfits']:
        avatar['outfit'] = outfit
        # Reset outfit variant if changing outfit category
        avatar['outfit_variant'] = AVATAR_OPTIONS['outfits'][outfit][0]
    
    # Update outfit variant if provided and valid
    if outfit_variant:
        if outfit_variant in AVATAR_OPTIONS['outfits'][avatar['outfit']]:
            avatar['outfit_variant'] = outfit_variant
    
    # Update accessories if provided
    if accessories and isinstance(accessories, list):
        valid_accessories = [acc for acc in accessories if acc in AVATAR_OPTIONS['accessories']]
        avatar['accessories'] = valid_accessories

def get_avatar_rgb_color():
    """Returns the actual RGB color tuple based on the chosen skin color name"""
    return AVATAR_OPTIONS['skin_colors'][player['avatar']['skin_color']]
