import numpy as np
from .vectors import dot, norm


def time_to_closest_point_of_approach(
    rel_pos: np.ndarray,
    rel_vel: np.ndarray,
    epsilon: float = 1e-6,
) -> float:
    """
    Deterministic time-to-CPA calculation.
    Returns 0.0 for degenerate or diverging cases.
    """
    vel_norm_sq = dot(rel_vel, rel_vel)

    if vel_norm_sq < epsilon:
        return 0.0

    t = -dot(rel_pos, rel_vel) / vel_norm_sq
    return max(0.0, float(t))


def distance_at_cpa(
    rel_pos: np.ndarray,
    rel_vel: np.ndarray,
) -> float:
    """
    Deterministic closest approach distance.
    """
    t_cpa = time_to_closest_point_of_approach(rel_pos, rel_vel)
    closest = rel_pos + rel_vel * t_cpa
    return norm(closest)
