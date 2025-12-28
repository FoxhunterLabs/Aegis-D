from typing import Tuple
from .levels import RiskLevel
from .parameters import RiskParameters


def compute_risk_score(
    distance_m: float,
    ttc_s: float,
    params: RiskParameters,
) -> float:
    """
    Deterministic heuristic risk score in [0.0, 1.0].
    Higher is worse.
    """

    distance_score = max(
        0.0,
        min(1.0, (params.high_distance_m - distance_m) / params.high_distance_m),
    )

    ttc_score = max(
        0.0,
        min(1.0, (params.high_ttc_s - ttc_s) / params.high_ttc_s),
    )

    return (
        params.distance_weight * distance_score
        + params.ttc_weight * ttc_score
    )


def map_score_to_level(
    distance_m: float,
    ttc_s: float,
    params: RiskParameters,
) -> RiskLevel:
    """
    Conservative threshold mapping.
    """

    if distance_m <= params.critical_distance_m or ttc_s <= params.critical_ttc_s:
        return RiskLevel.CRITICAL

    if distance_m <= params.high_distance_m or ttc_s <= params.high_ttc_s:
        return RiskLevel.HIGH

    return RiskLevel.LOW
