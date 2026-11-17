"""Усі налаштування та баланс гри в одному місці."""

# --- Інвентарі ---
POTION_SLOTS = 10
POTION_STACK = 10
INGREDIENT_SLOTS = 25
INGREDIENT_STACK = 25

# --- Економіка / прогресія ---
DAILY_INGREDIENTS = 5
START_GOLD = 100
DAILY_UPKEEP = 25          # оренда лабораторії щодня
GOAL_GOLD = 12000          # ціна Філософського каменя
MAX_DAYS = 60              # дедлайн Гільдії

# --- Випадковість ---
PRICE_FLUCT_MIN = 0.7
PRICE_FLUCT_MAX = 1.4
BONUS_RARITY = 3.5         # середня рідкість >= цього -> 2 зілля замість 1
RARITY_WEIGHTS = {1: 50, 2: 28, 3: 14, 4: 6, 5: 2}
