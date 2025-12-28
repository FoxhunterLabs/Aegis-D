import numpy as np


def norm(vec: np.ndarray) -> float:
    return float(np.linalg.norm(vec))


def unit(vec: np.ndarray) -> np.ndarray:
    n = norm(vec)
    if n == 0:
        return np.zeros_like(vec)
    return vec / n


def dot(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.dot(a, b))


def relative_position(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    return b - a


def relative_velocity(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    return b - a
