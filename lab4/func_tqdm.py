import time
from tqdm import tqdm


def progress_demo(n=20):
    for _ in tqdm(range(n), desc="Обробка"):
        time.sleep(0.05)