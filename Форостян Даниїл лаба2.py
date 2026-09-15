
users_db = {
    "oleksiy": {
        "password": "pin1",
        "grades": [10, 8, 4, 12, 3, 7]
    },
    "vadim": {
        "password": "pin2",
        "grades": [2, 5, 9, 11, 1, 6]
    },
    "danylo": {
        "password": "pin3",
        "grades": [8, 9, 10, 11, 12]
    },
    "ulia": {
        "password": "pin4",
        "grades": [3, 4, 2, 5, 8]
    }
}

def main():
    print("=== СИСТЕМА ПЕРЕГЛЯДУ ОЦІНОК ===")

    login = input("Введіть логін: ").strip()
    password = input("Введіть пароль: ").strip()

    if login in users_db and users_db[login]["password"] == password:
        print(f"\nУспішна авторизація! Вітаємо, {login}!")

        grades = users_db[login]["grades"]
        print(f"Ваші оцінки: {', '.join(map(str, grades))}")
        satisfactory = sum(1 for g in grades if 5 <= g <= 12)
        unsatisfactory = sum(1 for g in grades if 1 <= g <= 4)

        print("-" * 35)
        print(f"Кількість задовільних оцінок (5-12): {satisfactory}")
        print(f"Кількість незадовільних оцінок (1-4): {unsatisfactory}")
    else:
        print("\nПомилка: Невірний логін або пароль!")

if __name__ == "__main__":
    main()