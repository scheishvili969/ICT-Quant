"""Utility functions for loading price data from CSV files."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterable, List


@dataclass(frozen=True)
class PriceBar:
    """Represents a single OHLCV bar."""

    timestamp: datetime
    open: float
    high: float
    low: float
    close: float
    volume: float


def load_price_data(path: Iterable[str] | str | Path) -> List[PriceBar]:
    """Load price data from a CSV file.

    The CSV must contain a header with the following columns:
    ``timestamp,open,high,low,close,volume``. Timestamp values are parsed using
    :func:`datetime.fromisoformat`.
    """

    if isinstance(path, Iterable) and not isinstance(path, (str, Path)):
        lines = path
    else:
        lines = Path(path).read_text().splitlines()

    iterator = iter(lines)
    header = next(iterator, None)
    if header is None:
        raise ValueError("CSV file is empty")

    expected_header = "timestamp,open,high,low,close,volume"
    if header.strip().lower() != expected_header:
        raise ValueError(
            f"Unexpected header '{header}'. Expected '{expected_header}'."
        )

    bars: List[PriceBar] = []
    for line in iterator:
        if not line.strip():
            continue
        timestamp_str, open_, high, low, close, volume = line.split(",")
        bars.append(
            PriceBar(
                timestamp=datetime.fromisoformat(timestamp_str),
                open=float(open_),
                high=float(high),
                low=float(low),
                close=float(close),
                volume=float(volume),
            )
        )
    if not bars:
        raise ValueError("CSV file does not contain any price rows")
    return bars
