from enum import Enum


class TemporalStrategy(str, Enum):
    MAX = "max"     # conservative: never hides spikes
    MEAN = "mean"   # smoother, can hide spikes
    EMA = "ema"     # smooth + responsive, still can hide spikes
