"""Ринок: ціни та продаж зілль."""
import random

import config
from data.potions import POTIONS
from exceptions import MarketError, NotEnoughItemsError


def roll_prices(rng: random.Random) -> dict:
    """Ціни на сьогодні: базова ціна x випадкове коливання."""
    try:
        return {
            pid: max(1, round(r.base_price * rng.uniform(config.PRICE_FLUCT_MIN, config.PRICE_FLUCT_MAX)))
            for pid, r in POTIONS.items()
        }
    except (TypeError, ValueError) as e:
        raise MarketError("Не вдалося сформувати ціни.") from e


def sell(player, prices: dict, potion_id: str, amount: int) -> int:
    """Продає `amount` зілль. Повертає виручку."""
    try:
        price = prices[potion_id]
    except KeyError as e:
        raise MarketError("Для цього зілля немає ціни.") from e
    try:
        player.potions.remove(potion_id, amount)
    except NotEnoughItemsError as e:
        raise MarketError("У тебе немає стільки зілля.") from e
    earned = price * amount
    player.gold += earned
    player.total_sold += amount
    return earned


def sell_all(player, prices: dict) -> int:
    total = 0
    for potion_id, cnt in player.potions.summary():
        total += sell(player, prices, potion_id, cnt)
    return total
