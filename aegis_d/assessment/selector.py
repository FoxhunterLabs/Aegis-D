import uuid
from datetime import datetime
from typing import List, Dict

from ..constitution import SYSTEM_CONSTITUTION
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


SEVERITY_ORDER = {
    RiskLevel.NONE: 0,
    RiskLevel.LOW: 1,
    RiskLevel.ELEVATED: 2,
    RiskLevel.HIGH: 3,
    RiskLevel.CRITICAL: 4,
}


def select_most_concerning(
    detections: List[Dict[str, float]],
    params: RiskParameters = DEFAULT_RISK_PARAMETERS,
) -> RiskAssessment:
    """
    Deterministically select the most concerning detection.

    Tie-breaking hierarchy:
      1. Risk level (severity)
      2. Risk score
      3. Time-to-CPA (lower is worse)
      4. Distance (lower is worse)
    """

    if not detections:
        raise ValueError("detections must be non-empty")

    scored = []
    for d in detections:
        distance = float(d["distance_m"])
        ttc = float(d["ttc_s"])

        score = compute_risk_score(distance, ttc, params)
        level = map_score_to_level(distance, ttc, params)

        scored.append({
            "distance_m": distance,
            "ttc_s": ttc,
            "score": float(score),
            "level": level,
        })

    # Deterministic ordering: worst first
    scored.sort(
        key=lambda x: (
            SEVERITY_ORDER[x["level"]],
            x["score"],
            -x["ttc_s"],      # lower ttc is worse
            -x["distance_m"], # lower distance is worse
        ),
        reverse=True,
    )

    chosen = scored[0]

    hash_payload = {
        "detections": detections,             # caller-provided list, hash is still stable via sort_keys in json
        "parameters": params.__dict__,
        "constitution": SYSTEM_CONSTITUTION.to_dict(),
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
        constitution=SYSTEM_CONSTITUTION.to_dict(),
        input_hash=deterministic_hash(hash_payload),
        timestamp_utc=datetime.utcnow().isoformat(),
    )
