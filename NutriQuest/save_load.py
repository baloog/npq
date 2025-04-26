import json
from player_data import player
from datetime import datetime

def save_game():
    player['last_played'] = datetime.now().strftime("%Y-%m-%d")
    with open('nutriquest_save.json', 'w') as f:
        json.dump(player, f)

def load_game():
    global player
    try:
        with open('nutriquest_save.json', 'r') as f:
            player.update(json.load(f))
    except FileNotFoundError:
        pass
