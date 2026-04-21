import matplotlib.pyplot as plt
import pandas as pd


class Visualizer:
    def __init__(self, equity_curve, price_series=None, returns_series=None):
        self.equity = equity_curve
        self.price = price_series
        self.returns = returns_series

    def plot(self):

        fig, axs = plt.subplots(3, 1, figsize=(12, 10), sharex=True)

        # =========================
        # 1. EQUITY CURVE
        # =========================
        axs[0].plot(self.equity, label="Equity Curve", color="green")
        axs[0].set_title("Portfolio Equity Curve")
        axs[0].legend()

        # =========================
        # 2. STRATEGY RETURNS (NEW)
        # =========================
        if self.returns is not None:
            axs[1].plot(self.returns, label="Daily Returns", color="purple", alpha=0.7)
            axs[1].set_title("Strategy Daily Returns")
            axs[1].axhline(0, color="black", linewidth=1)
            axs[1].legend()

            # optional smoothing (rolling mean)
            rolling = pd.Series(self.returns).rolling(20).mean()
            axs[1].plot(rolling, label="20D Avg Return", color="orange")

        else:
            axs[1].text(0.5, 0.5, "No returns data provided",
                        ha="center", va="center")

        # =========================
        # 3. PRICE (OPTIONAL)
        # =========================
        if self.price is not None:
            axs[2].plot(self.price, label="Price", color="blue")
            axs[2].set_title("Reference Asset Price")
            axs[2].legend()
        else:
            axs[2].text(0.5, 0.5, "No price data provided",
                        ha="center", va="center")

        plt.tight_layout()
        plt.show()