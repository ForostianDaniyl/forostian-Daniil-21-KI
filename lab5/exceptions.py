"""Власні виключення гри."""


class GameError(Exception):
    """Базове виключення гри (показується гравцю як повідомлення)."""


class InventoryFullError(GameError):
    """В інвентарі немає місця."""


class NotEnoughItemsError(GameError):
    """Не вистачає предметів."""


class InvalidChoiceError(GameError):
    """Некоректний вибір гравця."""


class CraftError(GameError):
    """Помилка варіння зілля."""


class MarketError(GameError):
    """Помилка торгівлі."""


class DataError(Exception):
    """Помилка в даних гри (критична, гра не запуститься)."""


class GameQuit(Exception):
    """Гравець вийшов із гри (Ctrl+C / Ctrl+D / пункт «Вийти»)."""
