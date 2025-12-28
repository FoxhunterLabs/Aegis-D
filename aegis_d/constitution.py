from dataclasses import dataclass, asdict
from typing import Tuple, Dict, Any


@dataclass(frozen=True)
class SystemConstitution:
    """
    Machine-readable declaration of system capabilities and limitations.
    This is the non-negotiable truth contract for reviewers and integrators.
    """

    # CAPABILITIES
    deterministic: bool = True
    auditable: bool = True
    reproducible: bool = True
    input_order_independent: bool = True

    # LIMITATIONS
    certified: bool = False
    probabilistic: bool = False
    actuation_capable: bool = False
    hardware_validated: bool = False

    # PERFORMANCE ENVELOPE
    max_update_rate_hz: float = 10.0
    worst_case_latency_ms: float = 100.0
    memory_bound_mb: float = 50.0

    # INTENT
    intended_for: Tuple[str, ...] = (
        "research",
        "simulation",
        "prototyping",
        "education",
    )

    not_intended_for: Tuple[str, ...] = (
        "operational_use",
        "flight_control",
        "certification",
    )

    # DESIGN PHILOSOPHY
    design_principles: Tuple[str, ...] = (
        "determinism_over_optimization",
        "auditability_over_sophistication",
        "human_in_the_loop",
        "explicit_limitations",
    )

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


SYSTEM_CONSTITUTION = SystemConstitution()
