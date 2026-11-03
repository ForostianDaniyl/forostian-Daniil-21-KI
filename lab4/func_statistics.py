import statistics


def stats_demo():
    data = [4, 8, 15, 16, 23, 42]
    return {
        "mean": statistics.mean(data),
        "median": statistics.median(data),
        "stdev": round(statistics.stdev(data), 2),
    }