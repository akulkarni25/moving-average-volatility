import matplotlib.pyplot as plt
import yfinance as yf
import pandas as pd

class Visualizer:
    def __init__(self, portfolio_values, data_dict, start_date="2020-01-01", end_date="2024-01-01"):
        """
        portfolio_values: list or pd.Series of total portfolio values over time
        data_dict: dictionary of stock dataframes {ticker: df}
        start_date, end_date: used for downloading SPY benchmark
        """
        self.portfolio_values = pd.Series(portfolio_values, index=data_dict[list(data_dict.keys())[0]].index)
        self.data_dict = data_dict
        self.start_date = start_date
        self.end_date = end_date

    def plot(self):
        """
        Plots equity curves and benchmark comparisons.
        """
        fig, axs = plt.subplots(2, 1, figsize=(12, 10), sharex=True)

        # 1. Portfolio equity curve
        axs[0].plot(self.portfolio_values, label="Portfolio Strategy", color='green', linewidth=2)
        axs[0].set_title("Portfolio Equity Curve")
        axs[0].set_ylabel("Portfolio Value ($)")
        axs[0].legend()
        axs[0].grid(True)

        # 2. Compare against buy-and-hold and SPY
        axs[1].set_title("Strategy vs Buy & Hold vs S&P 500")
        for ticker, df in self.data_dict.items():
            buy_hold = df["Close"] / df["Close"].iloc[0] * 10000  # normalize to $10k initial capital
            axs[1].plot(df.index, buy_hold, linestyle="--", label=f"Buy & Hold ({ticker})")

        # SPY benchmark
        spy_df = yf.download("SPY", start=self.start_date, end=self.end_date).dropna()
        spy_df.index = spy_df.index.tz_localize(None)  # remove timezone
        spy_equity = spy_df["Close"] / spy_df["Close"].iloc[0] * 10000
        axs[1].plot(spy_df.index, spy_equity, linestyle=":", color="red", label="S&P 500 (SPY)")

        # Portfolio curve
        axs[1].plot(self.portfolio_values.index, self.portfolio_values, color='green', linewidth=2, label="Strategy")

        axs[1].set_ylabel("Portfolio Value ($)")
        axs[1].legend()
        axs[1].grid(True)

        plt.tight_layout()
        plt.show()

    @staticmethod
    def plot_equity_curves(portfolio_values, data_dict, start_date="2020-01-01", end_date="2024-01-01"):
        """
        Static method for quick plotting
        """
        viz = Visualizer(portfolio_values, data_dict, start_date, end_date)
        viz.plot()