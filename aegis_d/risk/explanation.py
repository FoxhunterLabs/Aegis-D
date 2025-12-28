from typing import Dict, Any
from .parameters import RiskParameters


def explain_risk_score(
    distance_m: float,
    ttc_s: float,
    params: RiskParameters,
) -> Dict[str, Any]:
    """
    Human-readable explanation of scoring inputs.
    """

    return {
        "distance_m": distance_m,
        "time_to_cpa_s": ttc_s,
        "weights": {
            "distance": params.distance_weight,
            "ttc": params.ttc_weight,
        },
        "thresholds": {
            "critical_distance_m": params.critical_distance_m,
            "critical_ttc_s": params.critical_ttc_s,
            "high_distance_m": params.high_distance_m,
            "high_ttc_s": params.high_ttc_s,
        },
    }
