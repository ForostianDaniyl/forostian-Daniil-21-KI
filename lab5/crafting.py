"""Логіка варіння зілль."""
from collections import Counter

import config
from data.ingredients import INGREDIENTS, get_ingredient
from data.potions import POTIONS, Recipe
from exceptions import CraftError, DataError, InventoryFullError, NotEnoughItemsError


def candidates(player, category: str) -> list:
    """id інгредієнтів з інвентаря героя, що підходять під категорію."""
    try:
        return [iid for iid, _ in player.ingredients.summary() if INGREDIENTS[iid].category == category]
    except KeyError as e:
        raise CraftError(f"Невідомий інгредієнт в інвентарі: {e}") from e


def can_craft(player, recipe: Recipe) -> bool:
    try:
        return all(candidates(player, cat) for cat in recipe.requires)
    except CraftError:
        return False


def craftable_recipes(player) -> list:
    return [r for r in POTIONS.values() if can_craft(player, r)]


def validate_choice(player, recipe: Recipe, chosen: list) -> None:
    try:
        if len(chosen) != len(recipe.requires):
            raise CraftError("Невірна кількість інгредієнтів.")
        got = Counter(get_ingredient(i).category for i in chosen)
        if got != Counter(recipe.requires):
            raise CraftError("Інгредієнти не підходять під цей рецепт.")
        for iid, need in Counter(chosen).items():
            if player.ingredients.count(iid) < need:
                raise NotEnoughItemsError("Не вистачає інгредієнтів.")
    except DataError as e:
        raise CraftError(str(e)) from e


def calc_yield(chosen: list) -> int:
    try:
        avg = sum(get_ingredient(i).rarity for i in chosen) / len(chosen)
        return 2 if avg >= config.BONUS_RARITY else 1
    except (DataError, ZeroDivisionError) as e:
        raise CraftError("Не вдалося порахувати вихід зілля.") from e


def brew(player, recipe: Recipe, chosen: list) -> int:
    """Варить зілля. Повертає кількість отриманих зілль."""
    validate_choice(player, recipe, chosen)
    produced = calc_yield(chosen)
    capacity = player.potions.capacity_for(recipe.id)
    if capacity == 0:
        raise InventoryFullError("Інвентар зілль повний — продай щось наприкінці дня!")
    produced = min(produced, capacity)
    for iid in chosen:
        player.ingredients.remove(iid, 1)
    player.potions.add(recipe.id, produced)
    player.potions_made += produced
    return produced
