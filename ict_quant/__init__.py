"""Lightweight quantitative trading toolkit.

This package provides utilities for loading price data, computing indicators,
and running basic backtests for simple trading strategies.
"""

from .data import load_price_data
from .indicators import moving_average
from .strategy import MovingAverageCrossStrategy
from .backtester import Backtester

__all__ = [
    "load_price_data",
    "moving_average",
    "MovingAverageCrossStrategy",
    "Backtester",
]
