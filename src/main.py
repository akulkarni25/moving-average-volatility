import yfinance as yf
import pandas as pd

from strategy import MovingAverageVolatilityStrategy
from backtester import Backtester
from performance import Performance
from visualizer import Visualizer


def main():

    # =========================
    # 1. DOWNLOAD DATA (SAFE)
    # =========================
    tickers = ["TSLA", "QLD"]

    raw = yf.download(
        tickers,
        start="2020-01-01",
        end="2024-01-01",
        group_by="ticker",
        auto_adjust=False
    )

    data_dict = {}

    for ticker in tickers:
        df = raw[ticker].copy()

        # clean + standardize
        df = df.dropna()
        df.index = pd.to_datetime(df.index)

        data_dict[ticker] = df


    # =========================
    # 2. RUN STRATEGY PER ASSET
    # =========================
    signals_dict = {}

    for ticker, df in data_dict.items():

        strategy = MovingAverageVolatilityStrategy(
            data=df,
            fast_window=20,
            slow_window=50,
            vol_window=20,
            vol_threshold=0.01,
            target_vol=0.02,
            max_leverage=2.0
        )

        signals_dict[ticker] = strategy.generate_signal()


    # =========================
    # 3. BACKTEST (CROSS-SECTIONAL)
    # =========================

    # align all dates
    common_index = data_dict[tickers[0]].index
    for ticker in tickers:
        common_index = common_index.intersection(data_dict[ticker].index)

    portfolio_returns = []

    for date in common_index:

        weights = {}

        for ticker in tickers:

            signal_df = signals_dict[ticker]
            val = signal_df.loc[date, "weight"]

            if isinstance(val, pd.Series):
                val = val.iloc[0]

            weights[ticker] = val

        total_abs = sum(abs(w) for w in weights.values())

        if total_abs == 0:
            normalized = {t: 0 for t in tickers}
        else:
            normalized = {t: w / total_abs for t, w in weights.items()}

        portfolio_return = 0

        for ticker in tickers:
            price_series = data_dict[ticker]["Close"]

            r = price_series.loc[date] / price_series.shift(1).loc[date] - 1

            r = 0 if pd.isna(r) else r

            portfolio_return += normalized[ticker] * r

        portfolio_returns.append(portfolio_return)

    portfolio_returns = pd.Series(portfolio_returns, index=common_index)

    results = (1 + portfolio_returns).cumprod()


    # =========================
    # 4. PERFORMANCE
    # =========================
    perf = Performance(results)
    metrics = perf.compute()

    print("\nPerformance Metrics:")
    for k, v in metrics.items():
        print(f"{k}: {v:.4f}")


    # =========================
    # 5. VISUALIZATION
    # =========================
    viz = Visualizer(
        results,
        data_dict["TSLA"]["Close"],
        portfolio_returns
    )
    viz.plot()


if __name__ == "__main__":
    main()