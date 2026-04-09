import numpy as np

class Performance:
    def __init__(self, df):
        self.df = df

    def compute(self):
        returns = self.df['strategy_returns'].dropna()

        total_return = self.df['equity_curve'].iloc[-1] - 1
        sharpe = np.sqrt(252) * returns.mean() / returns.std()

        vol = np.sqrt(252) * returns.std()

        return {
            "Total Return": total_return,
            "Sharpe Ratio": sharpe,
            "Annual Volatility": vol,
        }