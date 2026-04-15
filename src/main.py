import yfinance as yf
import pandas as pd

from strategy import MovingAverageVolatilityStrategy
from backtester import Backtester
from performance import Performance
from visualizer import Visualizer


def main():
    # 1. Download data
    tickers = ["TSLA", "NVDA", "QLD"]
    data = yf.download(tickers, start="2026-01-01", end="2026-04-01")

    df = data["Close"]["NVDA"].to_frame(name="Close")

    # 2. Initialize strategy
    strategy = MovingAverageVolatilityStrategy(
        data=df,
        fast_window=20,
        slow_window=50,
        vol_window=20,
        vol_threshold=0.01,
        target_vol=0.02,
        max_leverage=2.0
    )

    # 3. Run backtest
    backtester = Backtester(df, strategy)
    results = backtester.run()

    # 4. Performance
    perf = Performance(results)
    metrics = perf.performance_summary(results)
    print(metrics)

    # 5. Plot
    viz = Visualizer(results)
    viz.plot()


if __name__ == "__main__":
    main()