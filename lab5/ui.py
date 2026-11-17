"""Весь ввід/вивід. Єдине місце, де викликається input()."""
from crafting import can_craft
from data.ingredients import CATEGORIES, RARITY_NAMES, get_ingredient
from data.potions import get_recipe
from exceptions import DataError, GameQuit, InvalidChoiceError


def safe_input(prompt: str = "> ") -> str:
    try:
        return input(prompt).strip()
    except (EOFError, KeyboardInterrupt) as e:
        raise GameQuit from e


def ask_int(prompt: str, lo: int, hi: int) -> int:
    while True:
        try:
            value = int(safe_input(prompt))
            if not lo <= value <= hi:
                raise InvalidChoiceError
            return value
        except ValueError:
            print("  Введи число.")
        except InvalidChoiceError:
            print(f"  Число має бути від {lo} до {hi}.")


def confirm(prompt: str) -> bool:
    return safe_input(f"{prompt} (т/н): ").lower() in ("т", "так", "y", "yes")


def ingredient_label(ing_id: str) -> str:
    try:
        ing = get_ingredient(ing_id)
        return f"{ing.name} [{CATEGORIES[ing.category][0]}, {RARITY_NAMES[ing.rarity]}]"
    except (DataError, KeyError):
        return f"??? ({ing_id})"


def recipe_label(recipe) -> str:
    cats = " + ".join(CATEGORIES[c][0] for c in recipe.requires)
    return f"{recipe.name} ← {cats} (≈{recipe.base_price}з)"


def potion_label(potion_id: str) -> str:
    try:
        return get_recipe(potion_id).name
    except DataError:
        return f"??? ({potion_id})"


def show_ingredients(player) -> None:
    inv = player.ingredients
    print(f"\n=== Інгредієнти [{inv.used_slots}/{inv.max_slots} слотів, стак {inv.stack_size}] ===")
    items = inv.summary()
    if not items:
        print("  (порожньо)")
    for i, (iid, cnt) in enumerate(items, 1):
        print(f"{i:>3}. {ingredient_label(iid)} ×{cnt}")


def show_potions(player, prices: dict = None) -> None:
    inv = player.potions
    print(f"\n=== Зілля [{inv.used_slots}/{inv.max_slots} слотів, стак {inv.stack_size}] ===")
    items = inv.summary()
    if not items:
        print("  (порожньо)")
    for i, (pid, cnt) in enumerate(items, 1):
        price = f" — {prices[pid]}з/шт" if prices and pid in prices else ""
        print(f"{i:>3}. {potion_label(pid)} ×{cnt}{price}")


def show_recipes(recipes: list, player) -> None:
    print(f"\n=== Рецепти ({len(recipes)}) ===")
    for i, r in enumerate(recipes, 1):
        mark = "✓" if can_craft(player, r) else " "
        print(f"{i:>3}. [{mark}] {recipe_label(r)}")


def pick_option(title: str, options: list, label_fn):
    """Меню вибору. Повертає елемент або None, якщо гравець скасував."""
    if not options:
        return None
    print(f"\n{title}")
    for i, opt in enumerate(options, 1):
        print(f"{i:>3}. {label_fn(opt)}")
    print("  0. Скасувати")
    idx = ask_int("> ", 0, len(options))
    return None if idx == 0 else options[idx - 1]
