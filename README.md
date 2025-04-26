NutriQuest/
│
├── main.py             # 🔵 Main game launcher (controls the flow between pages)
├── constants.py        # 🟡 All colors, fonts, and screen settings
├── player_data.py      # 🟣 Player info (name, avatar, level, xp, meals)
├── food_database.py    # 🥗 All food nutrition data
├── save_load.py        # 💾 Save and load player progress
│
├── states/             # 🎮 Pages / Screens
│   ├── welcome.py         # Welcome screen
│   ├── create_avatar.py   # Avatar creation page
│   ├── home.py            # Home page
│   ├── track_meal.py      # Track Meal screen
│   ├── mini_game.py       # Mini-game screen
│   ├── level_up.py        # Level Up screen
│   └── advice.py          # Nutrition Advice screen
│
├── assets/            # 🎨 (Optional) Images, sounds, fonts, etc
│   ├── images/
│   └── sounds/
│
└── README.md           # 📄 Instructions for the project
