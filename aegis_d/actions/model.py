from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class ActionRecommendation:
    """
    Non-authoritative action suggestion.
    Requires explicit human approval before any execution.
    """
    recommendation: str
    rationale: str
    requires_human_approval: bool
    physical_constraints: Optional[str] = None
