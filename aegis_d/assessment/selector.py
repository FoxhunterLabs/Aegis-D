import uuid
from datetime import datetime
from typing import List, Dict, Any

from ..risk import (
    RiskLevel,
    compute_risk_score,
    map_score_to_level,
    explain_risk_score,
    RiskParameters,
    DEFAULT_RISK_PARAMETERS,
)
from .hashing import deterministic_hash
from .model import RiskAssessment


def select_most_concerning(
    detections: List[Dict[str, float]],
    params: RiskParameters = DEFAULT_RISK_PARAMETERS,
) -> RiskAssessment:
    """
    Deterministically select the most concerning detection.
    Tie-breaking hierarchy:
      1. Risk level
      2. Risk score
      3. Time-to-CPA (lower is worse)
      4. Stable ordering fallback
    """

    scored = []

    for d in detections:
        distance = d["distance_m"]
        ttc = d["ttc_s"]

        score = compute_risk_score(distance, ttc, params)
        level = map_score_to_level(distance, ttc, params)

        scored.append({
            "distance_m": distance,
            "ttc_s": ttc,
            "score": score,
            "level": level,
        })

    scored.sort(
        key=lambda x: (
            list(RiskLevel).index(x["level"]),
            -x["score"],
            x["ttc_s"],
        ),
        reverse=True,
    )

    chosen = scored[0]

    hash_payload = {
        "detections": detections,
        "parameters": params.__dict__,
    }

    return RiskAssessment(
        assessment_id=str(uuid.uuid4()),
        risk_level=chosen["level"],
        risk_score=chosen["score"],
        distance_m=chosen["distance_m"],
        ttc_s=chosen["ttc_s"],
        explanation=explain_risk_score(
            chosen["distance_m"],
            chosen["ttc_s"],
            params,
        ),
        parameters=params.__dict__,
        input_hash=deterministic_hash(hash_payload),
        timestamp_utc=datetime.utcnow().isoformat(),
    )
