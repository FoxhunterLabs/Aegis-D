from .model import ActionRecommendation
from .gates import requires_human_approval
from ..assessment.model import RiskAssessment
from ..risk.levels import RiskLevel


def recommend_action(assessment: RiskAssessment) -> ActionRecommendation:
    """
    Provide a conservative, non-binding recommendation.
    """

    level = assessment.risk_level

    if level == RiskLevel.NONE:
        return ActionRecommendation(
            recommendation="No action",
            rationale="No measurable risk detected",
            requires_human_approval=False,
        )

    if level == RiskLevel.LOW:
        return ActionRecommendation(
            recommendation="Increase monitoring",
            rationale="Low risk detected; maintain awareness",
            requires_human_approval=False,
        )

    if level == RiskLevel.ELEVATED:
        return ActionRecommendation(
            recommendation="Prepare mitigation options",
            rationale="Elevated risk; human review advised",
            requires_human_approval=True,
        )

    if level == RiskLevel.HIGH:
        return ActionRecommendation(
            recommendation="Initiate risk mitigation planning",
            rationale="High risk; human approval required",
            requires_human_approval=True,
            physical_constraints="Do not exceed system performance envelope",
        )

    if level == RiskLevel.CRITICAL:
        return ActionRecommendation(
            recommendation="Immediate human intervention required",
            rationale="Critical risk detected",
            requires_human_approval=True,
            physical_constraints="No autonomous action permitted",
        )

    raise ValueError(f"Unhandled risk level: {level}")
