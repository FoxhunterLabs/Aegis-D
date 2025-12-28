from collections import deque
from dataclasses import replace
from typing import Deque, Optional

from ..assessment.model import RiskAssessment
from ..risk.levels import RiskLevel
from ..assessment.selector import SEVERITY_ORDER
from .strategies import TemporalStrategy


def _worst_level(levels) -> RiskLevel:
    return max(levels, key=lambda lv: SEVERITY_ORDER[lv])


class TemporalAggregator:
    """
    Optional temporal smoothing layer.

    Defaults conservative (MAX) so transient spikes are preserved.
    """

    def __init__(
        self,
        window_size: int = 10,
        strategy: TemporalStrategy = TemporalStrategy.MAX,
        ema_alpha: float = 0.4,
    ):
        if window_size <= 0:
            raise ValueError("window_size must be > 0")
        if not (0.0 < ema_alpha <= 1.0):
            raise ValueError("ema_alpha must be in (0.0, 1.0]")

        self.window_size = window_size
        self.strategy = strategy
        self.ema_alpha = float(ema_alpha)
        self._buf: Deque[RiskAssessment] = deque(maxlen=window_size)
        self._ema_state: Optional[float] = None

    def update(self, assessment: RiskAssessment) -> RiskAssessment:
        """
        Add an assessment and return an aggregated assessment.
        Aggregation is deterministic for a given input sequence.
        """
        self._buf.append(assessment)
        return self.aggregate()

    def aggregate(self) -> RiskAssessment:
        if not self._buf:
            raise ValueError("No assessments available to aggregate")

        items = list(self._buf)
        levels = [a.risk_level for a in items]
        worst = _worst_level(levels)

        if self.strategy == TemporalStrategy.MAX:
            # choose the single worst assessment (by level then score)
            chosen = max(
                items,
                key=lambda a: (SEVERITY_ORDER[a.risk_level], a.risk_score),
            )
            return chosen

        if self.strategy == TemporalStrategy.MEAN:
            mean_score = sum(a.risk_score for a in items) / len(items)
            # keep "worst" level conservative; keep latest distance/ttc for context
            latest = items[-1]
            return replace(latest, risk_level=worst, risk_score=float(mean_score))

        if self.strategy == TemporalStrategy.EMA:
            latest = items[-1]
            if self._ema_state is None:
                self._ema_state = latest.risk_score
            else:
                self._ema_state = (
                    self.ema_alpha * latest.risk_score
                    + (1.0 - self.ema_alpha) * self._ema_state
                )
            return replace(latest, risk_level=worst, risk_score=float(self._ema_state))

        raise ValueError(f"Unknown strategy: {self.strategy}")
