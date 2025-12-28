from enum import Enum


class RiskLevel(str, Enum):
    NONE = "none"
    LOW = "low"
    ELEVATED = "elevated"
    HIGH = "high"
    CRITICAL = "critical"
