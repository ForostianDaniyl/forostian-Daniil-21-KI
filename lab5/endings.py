"""Кінцівки гри: перемога або поразка."""
from typing import NamedTuple, Optional

import config


class Ending(NamedTuple):
    is_win: bool
    title: str
    text: str


def check_victory(player) -> Optional[Ending]:
    try:
        if player.gold >= config.GOAL_GOLD:
            return Ending(
                True, "🏆 ПЕРЕМОГА: Філософський камінь",
                f"На {player.day}-й день ти кладеш на стіл Гільдії {config.GOAL_GOLD} золотих.\n"
                "Старий магістр мовчки дістає червоний камінь, що пульсує теплом.\n"
                "Ти більше не жебрак-алхімік — ти тепер Великий Магістр, а твоє ім'я\n"
                "вписане в літопис разом з найвеличнішими творцями еліксирів."
            )
    except TypeError:
        pass
    return None


def check_defeat(player, upkeep_paid: bool) -> Optional[Ending]:
    try:
        if not upkeep_paid:
            return Ending(
                False, "💀 ПОРАЗКА: виселення",
                f"Ти не зміг заплатити {config.DAILY_UPKEEP} золотих оренди.\n"
                "Орендодавець виставляє твої казани за двері, а колби розбиваються об бруківку.\n"
                "Мрія про Філософський камінь залишається лише мрією..."
            )
        if player.day >= config.MAX_DAYS:
            return Ending(
                False, "💀 ПОРАЗКА: дедлайн Гільдії",
                f"Минуло {config.MAX_DAYS} днів, а в тебе лише {player.gold} із {config.GOAL_GOLD} золотих.\n"
                "Гільдія оголошує пропозицію недійсною, а камінь дістається багатшому конкуренту.\n"
                "Ти залишаєшся звичайним алхіміком. Можливо, наступного разу пощастить."
            )
    except TypeError:
        pass
    return None
