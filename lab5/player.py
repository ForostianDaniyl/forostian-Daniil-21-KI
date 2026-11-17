"""Стан героя."""
from dataclasses import dataclass, field

import config
from inventory import Inventory


def _ingredient_inv() -> Inventory:
    return Inventory("Інгредієнти", config.INGREDIENT_SLOTS, config.INGREDIENT_STACK)


def _potion_inv() -> Inventory:
    return Inventory("Зілля", config.POTION_SLOTS, config.POTION_STACK)


@dataclass
class Player:
    name: str
    gold: int = config.START_GOLD
    day: int = 1
    total_sold: int = 0
    potions_made: int = 0
    ingredients: Inventory = field(default_factory=_ingredient_inv)
    potions: Inventory = field(default_factory=_potion_inv)
