from dataclasses import dataclass


@dataclass(frozen=True)
class RiskParameters:
    """
    Explicit, conservative scoring parameters.
    All values are inspectable and versionable.
    """

    distance_weight: float = 0.6
    ttc_weight: float = 0.4

    critical_distance_m: float = 2.0
    high_distance_m: float = 5.0

    critical_ttc_s: float = 2.0
    high_ttc_s: float = 5.0


DEFAULT_RISK_PARAMETERS = RiskParameters()
