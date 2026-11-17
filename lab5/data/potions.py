"""50 рецептів зілль: 45 пар категорій + 5 трійок."""
import random
from dataclasses import dataclass
from itertools import combinations

from data.ingredients import CATEGORIES
from exceptions import DataError

_NAMES = [
    "Зілля Зцілення", "Еліксир Сили", "Настій Спритності", "Зілля Невидимості", "Еліксир Мудрості",
    "Протиотрута", "Зілля Нічного Зору", "Настій Витривалості", "Зілля Сну", "Еліксир Бадьорості",
    "Зілля Швидкості", "Зілля Вогнестійкості", "Настій Холодостійкості", "Зілля Левітації",
    "Еліксир Удачі", "Зілля Підводного Дихання", "Зілля Мовлення Тварин", "Настій Кам'яної Шкіри",
    "Зілля Гніву", "Еліксир Краси", "Зілля Хоробрості", "Зілля Правди", "Настій Спокою",
    "Зілля Телепатії", "Еліксир Молодості", "Зілля Прозріння", "Настій Міцного Сну",
    "Зілля Хамелеона", "Зілля Тіні", "Еліксир Життя", "Зілля Лікантропії", "Зілля Росту",
    "Зілля Зменшення", "Настій Лісового Чарування", "Зілля Блискавки", "Зілля Магічного Щита",
    "Еліксир Мани", "Зілля Привидного Кроку", "Зілля Пошуку Скарбів", "Настій Першої Допомоги",
    "Зілля Забуття", "Зілля Пам'яті", "Зілля Кохання", "Зілля Морозного Дотику", "Вогняний Подих",
    "Еліксир Безсмертя", "Зілля Драконячої Люті", "Зілля Всевидіння", "Еліксир Архімага",
    "Універсальна Панацея",
]


@dataclass(frozen=True)
class Recipe:
    id: str
    name: str
    requires: tuple      # категорії інгредієнтів
    base_price: int


def _build() -> dict:
    try:
        cats = list(CATEGORIES)
        combos = list(combinations(cats, 2))
        triples = random.Random(7).sample(list(combinations(cats, 3)), 5)  # фіксований набір
        combos += sorted(triples)
        if len(combos) != len(_NAMES):
            raise DataError(f"Рецептів {len(combos)}, назв {len(_NAMES)}")
        result = {}
        for i, (reqs, name) in enumerate(zip(combos, _NAMES), 1):
            value = sum(CATEGORIES[c][1] for c in reqs)
            price = int(round(40 * value / 5.0)) * 5
            rid = f"potion_{i:02d}"
            result[rid] = Recipe(rid, name, tuple(reqs), price)
        if len(result) < 50:
            raise DataError("Потрібно мінімум 50 зілль")
        return result
    except (ValueError, KeyError) as e:
        raise DataError(f"Не вдалося побудувати рецепти: {e}") from e


POTIONS = _build()


def get_recipe(potion_id: str) -> Recipe:
    try:
        return POTIONS[potion_id]
    except KeyError as e:
        raise DataError(f"Невідоме зілля: {potion_id}") from e
