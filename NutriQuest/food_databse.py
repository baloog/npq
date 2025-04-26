food_database = {
    'apple': {'calories': 95, 'protein': 0.5, 'carbs': 25, 'fat': 0.3, 'vitamins': 8},
    'banana': {'calories': 105, 'protein': 1.3, 'carbs': 27, 'fat': 0.4, 'vitamins': 9},
    'broccoli': {'calories': 55, 'protein': 3.7, 'carbs': 11, 'fat': 0.6, 'vitamins': 15},
    'chicken': {'calories': 165, 'protein': 31, 'carbs': 0, 'fat': 3.6, 'vitamins': 5},
    'salmon': {'calories': 208, 'protein': 20, 'carbs': 0, 'fat': 13, 'vitamins': 11},
    'rice': {'calories': 130, 'protein': 2.7, 'carbs': 28, 'fat': 0.3, 'vitamins': 2},
    'pizza': {'calories': 285, 'protein': 12, 'carbs': 36, 'fat': 10, 'vitamins': 4},
    'soda': {'calories': 140, 'protein': 0, 'carbs': 39, 'fat': 0, 'vitamins': 0},
    'chocolate': {'calories': 210, 'protein': 2, 'carbs': 24, 'fat': 13, 'vitamins': 1},
    'salad': {'calories': 45, 'protein': 1.5, 'carbs': 8, 'fat': 0.5, 'vitamins': 12},
    'nuts': {'calories': 170, 'protein': 6, 'carbs': 5, 'fat': 14, 'vitamins': 7},
    'yogurt': {'calories': 120, 'protein': 10, 'carbs': 8, 'fat': 4, 'vitamins': 8}
}

def fetch_food_data(food_name):
    return food_database.get(food_name.lower(), {'calories': 100, 'protein': 2, 'carbs': 15, 'fat': 5, 'vitamins': 3})

def calculate_nutritional_score(food):
    score = food['protein'] * 3 + food['vitamins'] * 4 - food['fat']
    if food['carbs'] > 30:
        score -= (food['carbs'] - 30) / 2
    return max(5, score)
