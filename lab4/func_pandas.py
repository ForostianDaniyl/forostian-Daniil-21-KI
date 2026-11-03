import pandas as pd


def pandas_demo():
    df = pd.DataFrame({
        "name": ["Anna", "Oleh", "Iryna", "Taras"],
        "age": [21, 25, 19, 30],
        "score": [88, 92, 75, 81],
    })
    return df[["age", "score"]].describe().round(2)