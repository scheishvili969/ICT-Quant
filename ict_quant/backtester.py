"""A minimal event-driven backtesting engine."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List, Sequence

from .data import PriceBar


@dataclass(frozen=True)
class BacktestResult:
    """Summary statistics produced by :class:`Backtester`."""

    equity_curve: List[float]
    positions: List[int]
    total_return: float
    num_trades: int
    max_drawdown: float


class Backtester:
    """Simulate a simple long-only strategy using close-to-close returns."""

    def __init__(self, initial_capital: float = 10_000.0, trading_cost: float = 0.001):
        if initial_capital <= 0:
            raise ValueError("initial_capital must be positive")
        if trading_cost < 0:
            raise ValueError("trading_cost must be non-negative")
        self.initial_capital = float(initial_capital)
        self.trading_cost = float(trading_cost)

    def run(self, bars: Sequence[PriceBar], signals: Iterable[int]) -> BacktestResult:
        prices = list(bars)
        if not prices:
            raise ValueError("bars must not be empty")
        signal_list = list(signals)
        if len(signal_list) != len(prices):
            raise ValueError("signals and bars must have equal length")

        capital = self.initial_capital
        position = 0
        positions: List[int] = []
        trades = 0

        def apply_signal(signal: int) -> None:
            nonlocal capital, position, trades
            if signal == 1 and position <= 0:
                if position == 0:
                    capital -= capital * self.trading_cost
                    trades += 1
                position = 1
            elif signal == -1 and position >= 0:
                if position == 1:
                    capital -= capital * self.trading_cost
                    trades += 1
                position = 0

        apply_signal(signal_list[0])
        equity_curve: List[float] = [capital]
        positions.append(position)

        prev_close = prices[0].close
        max_equity = capital
        max_drawdown = 0.0

        for i in range(1, len(prices)):
            bar = prices[i]
            ret = (bar.close / prev_close) - 1.0
            capital *= 1.0 + position * ret
            apply_signal(signal_list[i])
            positions.append(position)
            equity_curve.append(capital)
            prev_close = bar.close
            if capital > max_equity:
                max_equity = capital
            drawdown = (max_equity - capital) / max_equity if max_equity else 0.0
            if drawdown > max_drawdown:
                max_drawdown = drawdown

        total_return = (capital / self.initial_capital) - 1.0
        return BacktestResult(
            equity_curve=equity_curve,
            positions=positions,
            total_return=total_return,
            num_trades=trades,
            max_drawdown=max_drawdown,
        )
