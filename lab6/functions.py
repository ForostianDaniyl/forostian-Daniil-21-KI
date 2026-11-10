from decorators import remove_vowels


@remove_vowels
def get_text():
    return "Привіт, це лабораторна робота номер шість! Hello, world!"


@remove_vowels
def greet(name):
    return f"Доброго дня, {name}! Good morning!"