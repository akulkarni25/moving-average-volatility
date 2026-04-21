import numpy as np
import pandas as pd
import yfinance as yf

class Performance:
    def __init__(self, portfolio_values, data_dict, start_date="2020-01-01", end_date="2024-01-01"):
        """
        portfolio_values: list or pd.Series of portfolio total values over time
        data_dict: dict of stock DataFrames {ticker: df}
        """
        self.portfolio_values = pd.Series(portfolio_values, index=data_dict[list(data_dict.keys())[0]].index)
        self.data_dict = data_dict
        self.start_date = start_date
        self.end_date = end_date

    def compute_portfolio_metrics(self, series):
        """
        Compute metrics for a given equity curve
        """
        returns = series.pct_change().dropna()
        total_return = series.iloc[-1] / series.iloc[0] - 1
        sharpe = (returns.mean() / returns.std()) * np.sqrt(252)
        vol = np.sqrt(252) * returns.std()
        max_dd = ((series / series.cummax()) - 1).min()
        return {
            "Total Return": total_return,
            "Sharpe Ratio": sharpe,
            "Annual Volatility": vol,
            "Max Drawdown": max_dd
        }

    def performance_summary(self):
        """
        Returns a DataFrame comparing portfolio strategy, buy-and-hold stocks, and S&P 500
        """
        results = {}

        # Portfolio strategy
        results["Strategy"] = self.compute_portfolio_metrics(self.portfolio_values)

        # Buy-and-hold for each stock
        for ticker, df in self.data_dict.items():
            buy_hold = df["Close"] / df["Close"].iloc[0] * 10000  # normalize to initial $10k
            results[f"Buy & Hold ({ticker})"] = self.compute_portfolio_metrics(buy_hold)

        # S&P 500 benchmark
        spy_df = yf.download("SPY", start=self.start_date, end=self.end_date).dropna()
        spy_df.index = spy_df.index.tz_localize(None)
        spy_equity = spy_df["Close"] / spy_df["Close"].iloc[0] * 10000
        results["S&P 500 (SPY)"] = self.compute_portfolio_metrics(spy_equity)

        summary_df = pd.DataFrame(results).T
        return summary_df