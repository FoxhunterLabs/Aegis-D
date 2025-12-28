from dataclasses import dataclass
from typing import Dict, Any
from datetime import datetime
from ..risk import RiskLevel


@dataclass(frozen=True)
class RiskAssessment:
    """
    Complete, auditable risk assessment record.
    """
    assessment_id: str
    risk_level: RiskLevel
    risk_score: float
    distance_m: float
    ttc_s: float
    explanation: Dict[str, Any]
    parameters: Dict[str, Any]
    input_hash: str
    timestamp_utc: str
