from functools import wraps

VOWELS = "аеєиіїоуюяАЕЄИІЇОУЮЯaeiouAEIOU"


def remove_vowels(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)  # отримуємо рядок від оригінальної функції
        return "".join(ch for ch in result if ch not in VOWELS)
    return wrapper