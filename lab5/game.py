"""Головний ігровий цикл."""
import random

import config
import crafting
import daily
import endings
import market
import ui
from data.potions import POTIONS
from exceptions import DataError, GameError, GameQuit, InventoryFullError, MarketError
from player import Player

MENU = """
--- День {day}/{max_days} | Золото: {gold} | Ціль: {goal} ---
 1. Інгредієнти        5. Викинути інгредієнт
 2. Зілля              6. Ціни на ринку
 3. Книга рецептів     7. Завершити день (продаж)
 4. Варити зілля       0. Вийти"""


class Game:
    def __init__(self, rng: random.Random = None):
        self.rng = rng or random.Random()
        self.player = None
        self.prices = {}

    # ---------- запуск ----------
    def run(self) -> None:
        try:
            self._intro()
            while True:
                ending = self._play_day()
                if ending:
                    self._show_ending(ending)
                    return
        except GameQuit:
            print("\nГру перервано. До зустрічі, алхіміку!")
        except DataError as e:
            print(f"\nКритична помилка даних гри: {e}")
        except Exception as e:  # остання лінія захисту
            print(f"\nНепередбачена помилка: {type(e).__name__}: {e}")

    def _intro(self) -> None:
        print("=" * 60)
        print("  АЛХІМІК: шлях до Філософського каменя")
        print("=" * 60)
        print(f"Гільдія продає Філософський камінь за {config.GOAL_GOLD} золотих.")
        print(f"Маєш {config.MAX_DAYS} днів. Оренда лабораторії — {config.DAILY_UPKEEP}з щодня.")
        print(f"Щодня отримуєш {config.DAILY_INGREDIENTS} інгредієнтів, варіш зілля і продаєш їх увечері.")
        name = ui.safe_input("Ім'я алхіміка: ") or "Алхімік"
        self.player = Player(name=name, gold=config.START_GOLD)

    # ---------- день ----------
    def _play_day(self):
        p = self.player
        try:
            self.prices = market.roll_prices(self.rng)
        except MarketError as e:
            print(f"⚠ {e}")
            self.prices = {pid: r.base_price for pid, r in POTIONS.items()}
        print(f"\n☀ Настає день {p.day}. {p.name}, ось твоя поставка інгредієнтів!")
        self._receive_daily_ingredients()
        while True:
            print(MENU.format(day=p.day, max_days=config.MAX_DAYS, gold=p.gold, goal=config.GOAL_GOLD))
            choice = ui.ask_int("> ", 0, 7)
            try:
                if choice == 0:
                    if ui.confirm("Справді вийти?"):
                        raise GameQuit
                elif choice == 1:
                    ui.show_ingredients(p)
                elif choice == 2:
                    ui.show_potions(p, self.prices)
                elif choice == 3:
                    self._show_recipe_book()
                elif choice == 4:
                    self._brew_menu()
                elif choice == 5:
                    self._discard_menu()
                elif choice == 6:
                    ui.show_potions(p, self.prices)
                    print("(ціни діють лише сьогодні)")
                elif choice == 7:
                    if ui.confirm("Завершити день?"):
                        break
            except GameError as e:
                print(f"⚠ {e}")
        return self._end_of_day()

    def _receive_daily_ingredients(self) -> None:
        p = self.player
        try:
            ids = daily.roll_ingredient_ids(self.rng)
        except DataError as e:
            print(f"⚠ {e}")
            return
        for iid in ids:
            label = ui.ingredient_label(iid)
            while True:
                try:
                    p.ingredients.add(iid, 1)
                    print(f"  + {label}")
                    break
                except InventoryFullError:
                    print(f"  ! Немає місця для: {label}")
                    if not self._make_room():
                        print(f"  – {label} залишено.")
                        break

    def _make_room(self) -> bool:
        """Пропонує викинути весь запас одного інгредієнта. True — місце звільнено."""
        try:
            items = self.player.ingredients.summary()
            pick = ui.pick_option("Що викинути, щоб звільнити слот?", items,
                                  lambda it: f"{ui.ingredient_label(it[0])} ×{it[1]}")
            if pick is None:
                return False
            self.player.ingredients.remove(pick[0], pick[1])
            return True
        except GameError as e:
            print(f"⚠ {e}")
            return False

    # ---------- меню дій ----------
    def _show_recipe_book(self) -> None:
        print("\n1. Доступні зараз   2. Усі рецепти")
        mode = ui.ask_int("> ", 1, 2)
        recipes = crafting.craftable_recipes(self.player) if mode == 1 else list(POTIONS.values())
        if not recipes:
            print("  Зараз не вистачає інгредієнтів ні для одного рецепта.")
            return
        ui.show_recipes(recipes, self.player)

    def _brew_menu(self) -> None:
        p = self.player
        recipes = crafting.craftable_recipes(p)
        if not recipes:
            print("  Немає інгредієнтів для жодного рецепта (див. «Книга рецептів»).")
            return
        recipe = ui.pick_option("Що варимо?", recipes, ui.recipe_label)
        if recipe is None:
            return
        chosen = []
        for category in recipe.requires:
            options = crafting.candidates(p, category)
            pick = ui.pick_option(f"Обери інгредієнт категорії «{crafting_cat_name(category)}»:", options,
                                  lambda i: f"{ui.ingredient_label(i)} ×{p.ingredients.count(i)}")
            if pick is None:
                print("  Варіння скасовано.")
                return
            chosen.append(pick)
        produced = crafting.brew(p, recipe, chosen)
        bonus = " (бонус за рідкісні інгредієнти!)" if produced == 2 else ""
        print(f"  ⚗ Готово: {recipe.name} ×{produced}{bonus}")

    def _discard_menu(self) -> None:
        items = self.player.ingredients.summary()
        pick = ui.pick_option("Який інгредієнт викинути?", items,
                              lambda it: f"{ui.ingredient_label(it[0])} ×{it[1]}")
        if pick is None:
            return
        amount = ui.ask_int(f"Скільки викинути (1-{pick[1]})? ", 1, pick[1])
        self.player.ingredients.remove(pick[0], amount)
        print("  Викинуто.")

    # ---------- кінець дня ----------
    def _sell_phase(self) -> None:
        p = self.player
        print("\n🌙 Кінець дня. Час продавати зілля.")
        while not p.potions.is_empty():
            items = p.potions.summary()
            ui.show_potions(p, self.prices)
            print("  Номер — продати вид | A — продати все | 0 — залишити решту")
            raw = ui.safe_input("> ").lower()
            try:
                if raw == "0":
                    break
                if raw == "a":
                    print(f"  💰 Виручка: {market.sell_all(p, self.prices)}з")
                    continue
                idx = int(raw)
                if not 1 <= idx <= len(items):
                    raise ValueError
                pid, cnt = items[idx - 1]
                amount = ui.ask_int(f"Скільки продати (1-{cnt}, 0 — усе)? ", 0, cnt) or cnt
                print(f"  💰 Виручка: {market.sell(p, self.prices, pid, amount)}з")
            except ValueError:
                print("  Невірний вибір.")
            except GameError as e:
                print(f"⚠ {e}")
        if p.potions.is_empty():
            print("  Усе продано.")

    def _end_of_day(self):
        p = self.player
        self._sell_phase()
        win = endings.check_victory(p)
        if win:
            return win
        paid = daily.pay_upkeep(p)
        if paid:
            print(f"🏠 Оренда: -{config.DAILY_UPKEEP}з. Залишилось: {p.gold}з.")
        defeat = endings.check_defeat(p, paid)
        if defeat:
            return defeat
        p.day += 1
        return None

    def _show_ending(self, ending) -> None:
        p = self.player
        print("\n" + "=" * 60)
        print(ending.title)
        print("=" * 60)
        print(ending.text)
        print(f"\nДнів: {p.day} | Золото: {p.gold} | Зварено зілль: {p.potions_made} | Продано: {p.total_sold}")


def crafting_cat_name(category: str) -> str:
    from data.ingredients import CATEGORIES
    return CATEGORIES.get(category, (category,))[0]
