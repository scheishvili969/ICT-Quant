"""Run a small moving average crossover backtest on sample data."""

from __future__ import annotations

from pathlib import Path

from ict_quant import (
    Backtester,
    MovingAverageCrossStrategy,
    load_price_data,
)


def main() -> None:
    data_path = Path(__file__).resolve().parent / "data" / "sample_prices.csv"
    bars = load_price_data(data_path)

    strategy = MovingAverageCrossStrategy(fast_window=5, slow_window=15)
    signals = strategy.generate_signals(bars)

    backtester = Backtester(initial_capital=5_000.0, trading_cost=0.0005)
    result = backtester.run(bars, signals)

    print("Moving Average Crossover Backtest")
    print("-" * 40)
    print(f"Final equity: ${result.equity_curve[-1]:,.2f}")
    print(f"Total return: {result.total_return * 100:.2f}%")
    print(f"Max drawdown: {result.max_drawdown * 100:.2f}%")
    print(f"Number of trades: {result.num_trades}")

    print("\nEquity curve (first 10 points):")
    for ts, equity in zip((bar.timestamp for bar in bars[:10]), result.equity_curve[:10]):
        print(f"{ts.date()}: ${equity:,.2f}")


if __name__ == "__main__":
    main()
