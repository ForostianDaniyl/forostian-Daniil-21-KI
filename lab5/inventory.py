"""Універсальний інвентар зі слотами та стаками."""
from exceptions import InvalidChoiceError, InventoryFullError, NotEnoughItemsError


class Inventory:
    def __init__(self, title: str, max_slots: int, stack_size: int):
        self.title = title
        self.max_slots = max_slots
        self.stack_size = stack_size
        self._stacks = []  # [[item_id, count], ...]

    @property
    def used_slots(self) -> int:
        return len(self._stacks)

    def is_empty(self) -> bool:
        return not self._stacks

    def count(self, item_id: str) -> int:
        return sum(c for i, c in self._stacks if i == item_id)

    def capacity_for(self, item_id: str) -> int:
        """Скільки ще одиниць цього предмета влізе."""
        in_stacks = sum(self.stack_size - c for i, c in self._stacks if i == item_id)
        free_slots = self.max_slots - len(self._stacks)
        return in_stacks + free_slots * self.stack_size

    def add(self, item_id: str, amount: int = 1) -> int:
        """Додає предмети. Повертає, скільки реально додано."""
        try:
            if amount <= 0:
                raise ValueError("amount must be > 0")
            capacity = self.capacity_for(item_id)
            if capacity == 0:
                raise InventoryFullError(f"{self.title}: немає місця.")
            to_add = min(amount, capacity)
            left = to_add
            for stack in self._stacks:
                if left == 0:
                    break
                if stack[0] == item_id and stack[1] < self.stack_size:
                    take = min(self.stack_size - stack[1], left)
                    stack[1] += take
                    left -= take
            while left > 0:
                take = min(self.stack_size, left)
                self._stacks.append([item_id, take])
                left -= take
            return to_add
        except ValueError as e:
            raise InvalidChoiceError("Некоректна кількість.") from e

    def remove(self, item_id: str, amount: int = 1) -> None:
        if amount <= 0:
            raise InvalidChoiceError("Некоректна кількість.")
        if self.count(item_id) < amount:
            raise NotEnoughItemsError("Не вистачає предметів в інвентарі.")
        left = amount
        for idx in range(len(self._stacks) - 1, -1, -1):
            if left == 0:
                break
            stack = self._stacks[idx]
            if stack[0] == item_id:
                take = min(stack[1], left)
                stack[1] -= take
                left -= take
        self._stacks = [s for s in self._stacks if s[1] > 0]

    def summary(self) -> list:
        """[(item_id, загальна_кількість), ...] у порядку появи."""
        totals = {}
        for item_id, cnt in self._stacks:
            totals[item_id] = totals.get(item_id, 0) + cnt
        return list(totals.items())
