import yfinance as yf
import pandas as pd

from strategy import MovingAverageVolatilityStrategy
from portfolio import initialize_positions, rebalance, compute_portfolio_value
from performance import Performance
from visualizer import Visualizer


def main():
    # 1. Download data
    tickers = ["TSLA", "QLD"]
    data_dict = {}

    for ticker in tickers:
        df = yf.download(ticker, start="2020-01-01", end="2024-01-01")
        df = df.dropna()
        df.index = df.index.tz_localize(None)  # remove timezone
        data_dict[ticker] = df

    # Align dates
    common_index = data_dict["TSLA"].index
    for ticker in tickers:
        data_dict[ticker] = data_dict[ticker].reindex(common_index).ffill()

    # 2. Generate signals using your strategy class (signals only)
    signals_dict = {}
    for ticker, df in data_dict.items():
        strat = MovingAverageVolatilityStrategy(
            data=df,
            fast_window=20,
            slow_window=50,
            vol_window=20,
            vol_threshold=0.01,
            target_vol=0.02,
            max_leverage=2.0
        )
        signals_dict[ticker] = strat.generate_signal()

    # 3. Initialize portfolio (both stocks start with $5000)
    initialize_positions(data_dict, initial_capital=5000)

    # 4. Run portfolio backtest
    portfolio_values = []
    for date in common_index:
        rebalance(date, data_dict, signals_dict)
        value = compute_portfolio_value(date, data_dict)
        portfolio_values.append(value)

    # 5. Performance evaluation
    perf = Performance(portfolio_values, data_dict)
    metrics = perf.performance_summary()
    print(metrics)

    # 6. Plot portfolio equity curve
    viz = Visualizer(portfolio_values, data_dict)
    viz.plot()


if __name__ == "__main__":
    main()