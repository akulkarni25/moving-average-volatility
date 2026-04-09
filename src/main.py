import yfinance as yf
import pandas as pd

from strategy import MovingAverageVolatilityStrategy
from backtester import Backtester
from performance import Performance
from visualizer import Visualizer


def main():
    # 1. Download data
    tickers = ["TSLA", "NVDA"]
    data = yf.download(tickers, start="2020-01-01", end="2024-01-01")

    df = data["Close"]["TSLA"].to_frame(name="Close")

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
    metrics = perf.compute()

    print("\nPerformance Metrics:")
    for k, v in metrics.items():
        print(f"{k}: {v:.4f}")

    # 5. Plot
    viz = Visualizer(results)
    viz.plot()


if __name__ == "__main__":
    main()