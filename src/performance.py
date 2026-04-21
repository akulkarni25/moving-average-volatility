import numpy as np
import pandas as pd


class Performance:
    def __init__(self, equity_curve: pd.Series):
        self.equity_curve = equity_curve.dropna()

    def compute(self):

        # =========================
        # 1. RETURNS
        # =========================
        returns = self.equity_curve.pct_change().dropna()

        # =========================
        # 2. METRICS
        # =========================
        total_return = (self.equity_curve.iloc[-1] /
                        self.equity_curve.iloc[0]) - 1

        sharpe = np.sqrt(252) * returns.mean() / (returns.std() + 1e-8)

        volatility = np.sqrt(252) * returns.std()

        # =========================
        # 3. DRAWDOWN (IMPORTANT ADDITION)
        # =========================
        rolling_max = self.equity_curve.cummax()
        drawdown = (self.equity_curve / rolling_max) - 1
        max_drawdown = drawdown.min()

        return {
            "Total Return": total_return,
            "Sharpe Ratio": sharpe,
            "Annual Volatility": volatility,
            "Max Drawdown": max_drawdown
        }