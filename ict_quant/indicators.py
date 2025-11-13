"""Technical indicators used by the strategies."""

from __future__ import annotations

from collections import deque
from typing import Iterable, Iterator, List


def moving_average(values: Iterable[float], window: int) -> List[float]:
    """Compute a simple moving average over *window* periods.

    The function returns a list that aligns with the provided values. The first
    ``window - 1`` entries will be ``NaN`` because a full window is not
    available yet.
    """

    if window <= 0:
        raise ValueError("window must be positive")

    history: deque[float] = deque(maxlen=window)
    result: List[float] = []
    total = 0.0

    for value in values:
        if len(history) == window:
            total -= history[0]
        history.append(value)
        total += value
        if len(history) == window:
            result.append(total / window)
        else:
            result.append(float("nan"))
    return result


def iter_moving_average(values: Iterable[float], window: int) -> Iterator[float]:
    """Yield moving average values lazily."""

    history: deque[float] = deque(maxlen=window)
    total = 0.0
    for value in values:
        if len(history) == window:
            total -= history[0]
        history.append(value)
        total += value
        if len(history) == window:
            yield total / window
        else:
            yield float("nan")
