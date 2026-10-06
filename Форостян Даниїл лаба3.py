def main():
    catalog = {
        "apple": {"name": "Яблуко", "price": 15.5, "stock": 50},
        "milk": {"name": "Молоко", "price": 38.0, "stock": 20},
        "bread": {"name": "Хліб", "price": 22.25, "stock": 15},
        "chocolate": {"name": "Шоколад", "price": 45.0, "stock": 30}
    }

    # Кошик користувача: (код товару: кількість)
    cart = {}

    format_price = lambda p: f"{p:.2f}грн"

    while True:
        print("\n=== КОНСОЛЬНИЙ МАГАЗИН ===")
        print("1. Переглянути каталог товарів")
        print("2. Додати товар у кошик")
        print("3. Видалити товар з кошика")
        print("4. Купити товари з кошика")
        print("5. Увійти як адміністратор (переглянути залишки)")
        print("6. Вийти з програми")

        choice = input("Оберіть дію (1-6): ").strip()

        if choice == "1":
            print("\n--- КАТАЛОГ ТОВАРІВ ---")
            sorted_items = sorted(catalog.items(), key=lambda item: item[1]['price'])
            for key, data in sorted_items:
                print(f"Код: {key} | {data['name']} — {format_price(data['price'])} (в наявності: {data['stock']} шт.)")

        elif choice == "2":
            item_code = input("Введіть код товару для додавання: ").strip().lower()
            if item_code in catalog:
                if catalog[item_code]["stock"] > 0:
                    cart[item_code] = cart.get(item_code, 0) + 1
                    catalog[item_code]["stock"] -= 1
                    print(f"Товар '{catalog[item_code]['name']}' успішно додано до кошика!")
                else:
                    print("Вибачте, цього товару більше немає на складі.")
            else:
                print("Помилка: товару з таким кодом не існує.")

        elif choice == "3":
            if not cart:
                print("Ваш кошик порожній.")
                continue

            print("\n--- ВАШ КОШИК ---")
            for code, qty in cart.items():
                print(f"Код: {code} | {catalog[code]['name']} — {qty} шт.")

            item_code = input("Введіть код товару для видалення з кошика: ").strip().lower()
            if item_code in cart:
                catalog[item_code]["stock"] += cart[item_code]
                del cart[item_code]
                print("Товар видалено з кошика, залишки на складі оновлено.")
            else:
                print("У вашому кошику немає такого товару.")

        elif choice == "4":
            if not cart:
                print("Ваш кошик порожній. Купівля неможлива.")
                continue

            print("\n--- ОФОРМЛЕННЯ ЗАМОВЛЕННЯ ---")
            total = 0
            for code, qty in cart.items():
                item_total = catalog[code]["price"] * qty
                total += item_total
                print(f"{catalog[code]['name']} x {qty} = {format_price(item_total)}")

            print(f"Загальна сума до сплати: {format_price(total)}")
            confirm = input("Підтвердити купівлю? (так/ні): ").strip().lower()

            if confirm in ("так", "yes", "y"):
                cart.clear()
                print("Дякуємо за покупку! Замовлення успішно оформлено.")
            else:
                print("Купівлю скасовано.")

        elif choice == "5":
            password = input("Введіть пароль адміністратора: ").strip()
            #(пароль: admin123)
            if password == "admin123":
                print("\n--- ПАНЕЛЬ АДМІНІСТРАТОРА: ЗАЛИШКИ ---")
                for key, data in catalog.items():
                    print(
                        f"Код: {key} | Назва: {data['name']} | Залишок: {data['stock']} шт. | Ціна: {format_price(data['price'])}")
            else:
                print("Неправильний пароль доступу!")

        elif choice == "6":
            print("Дякуємо, що користувалися нашим магазином! До побачення.")
            break
        else:
            print("Невірний вибір. Будь ласка, введіть число від 1 до 6.")


if __name__ == "__main__":
    main()