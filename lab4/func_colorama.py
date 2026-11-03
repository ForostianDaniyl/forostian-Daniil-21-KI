from colorama import Fore, Style, init

init(autoreset=True)

COLORS = {"red": Fore.RED, "green": Fore.GREEN, "cyan": Fore.CYAN, "yellow": Fore.YELLOW}


def print_colored(text, color="green"):
    print(COLORS.get(color, Fore.WHITE) + text + Style.RESET_ALL)