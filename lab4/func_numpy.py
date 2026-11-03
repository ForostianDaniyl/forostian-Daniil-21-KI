import numpy as np


def numpy_matrix_demo():
    a = np.arange(1, 10).reshape(3, 3)
    return {
        "matrix": a.tolist(),
        "transpose": a.T.tolist(),
        "sum": int(a.sum()),
        "det": round(float(np.linalg.det(a)), 2),
    }