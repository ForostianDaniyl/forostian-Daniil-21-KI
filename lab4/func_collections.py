from collections import Counter


def counter_demo():
    words = "to be or not to be that is the question".split()
    return Counter(words).most_common(3)