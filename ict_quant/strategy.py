"""Trading strategies."""

from __future__ import annotations

from dataclasses import dataclass
from math import isnan
from typing import Iterable, List

from .data import PriceBar
from .indicators import moving_average


@dataclass(frozen=True)
class MovingAverageCrossStrategy:
    """Simple moving average crossover strategy.

    When the fast moving average crosses above the slow moving average a long
    position is opened. When it crosses below, the position is closed.
    """

    fast_window: int = 5
    slow_window: int = 20

    def __post_init__(self) -> None:
        if self.fast_window <= 0 or self.slow_window <= 0:
            raise ValueError("window lengths must be positive")
        if self.fast_window >= self.slow_window:
            raise ValueError("fast window must be shorter than slow window")

    def generate_signals(self, bars: Iterable[PriceBar]) -> List[int]:
        closes = [bar.close for bar in bars]
        fast_ma = moving_average(closes, self.fast_window)
        slow_ma = moving_average(closes, self.slow_window)

        signals: List[int] = []
        position = 0
        for fast, slow in zip(fast_ma, slow_ma):
            if isnan(fast) or isnan(slow):
                signals.append(0)
                continue
            if fast > slow and position <= 0:
                position = 1
                signals.append(1)
            elif fast < slow and position >= 0:
                position = -1
                signals.append(-1)
            else:
                signals.append(0)
        return signals
