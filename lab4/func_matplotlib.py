import matplotlib
matplotlib.use("Agg")  # без вікна, зберігаємо у файл
import matplotlib.pyplot as plt


def make_plot(filename="plot.png"):
    x = list(range(1, 11))
    y = [i ** 2 for i in x]
    plt.figure()
    plt.plot(x, y, marker="o")
    plt.title("y = x^2")
    plt.grid(True)
    plt.savefig(filename)
    plt.close()
    return f"графік збережено у {filename}"