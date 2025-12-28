from ..risk.levels import RiskLevel


def requires_human_approval(level: RiskLevel) -> bool:
    """
    Human-in-the-loop gate.
    """
    return level in {RiskLevel.ELEVATED, RiskLevel.HIGH, RiskLevel.CRITICAL}
