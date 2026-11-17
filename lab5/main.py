"""Точка входу: python main.py"""
from game import Game


def main() -> None:
    try:
        Game().run()
    except Exception as e:
        print(f"Не вдалося запустити гру: {type(e).__name__}: {e}")


if __name__ == "__main__":
    main()
