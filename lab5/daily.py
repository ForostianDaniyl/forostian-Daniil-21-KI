"""Щоденні події: видача інгредієнтів та оплата оренди."""
import random

import config
from data.ingredients import INGREDIENTS
from exceptions import DataError


def roll_ingredient_ids(rng: random.Random, count: int = config.DAILY_INGREDIENTS) -> list:
    """Випадкові інгредієнти дня з урахуванням рідкості."""
    try:
        by_rarity = {}
        for ing in INGREDIENTS.values():
            by_rarity.setdefault(ing.rarity, []).append(ing.id)
        rarities = list(config.RARITY_WEIGHTS)
        weights = [config.RARITY_WEIGHTS[r] for r in rarities]
        result = []
        for _ in range(count):
            rarity = rng.choices(rarities, weights=weights)[0]
            result.append(rng.choice(by_rarity[rarity]))
        return result
    except (KeyError, IndexError) as e:
        raise DataError(f"Помилка генерації інгредієнтів дня: {e}") from e


def pay_upkeep(player) -> bool:
    """Списує оренду. False — якщо грошей не вистачило."""
    try:
        if player.gold < config.DAILY_UPKEEP:
            return False
        player.gold -= config.DAILY_UPKEEP
        return True
    except TypeError:
        return False
