from math import isclose, isnan
from pathlib import Path
import sys

import pytest

sys.path.append(str(Path(__file__).resolve().parents[1]))

from ict_quant import (
    Backtester,
    MovingAverageCrossStrategy,
    load_price_data,
    moving_average,
)


@pytest.fixture(scope="module")
def sample_bars() -> list:
    data_path = Path(__file__).resolve().parents[1] / "data" / "sample_prices.csv"
    return load_price_data(data_path)


def test_load_price_data(sample_bars: list) -> None:
    assert len(sample_bars) == 51
    first = sample_bars[0]
    assert first.close == pytest.approx(100.5)
    assert first.timestamp.year == 2024


def test_moving_average() -> None:
    values = [1, 2, 3, 4, 5]
    ma = moving_average(values, 3)
    assert isnan(ma[0])
    assert isnan(ma[1])
    assert isclose(ma[2], 2.0)
    assert isclose(ma[-1], 4.0)


def test_backtest_runs(sample_bars: list) -> None:
    strategy = MovingAverageCrossStrategy(fast_window=3, slow_window=7)
    signals = strategy.generate_signals(sample_bars)
    backtester = Backtester(initial_capital=1_000.0, trading_cost=0.0)
    result = backtester.run(sample_bars, signals)

    assert len(result.equity_curve) == len(sample_bars)
    assert result.total_return > -1.0
    assert result.num_trades > 0
    assert 0 <= result.max_drawdown < 1
