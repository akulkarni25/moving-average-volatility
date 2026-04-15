import numpy as np
import pandas as pd

class Performance:
    def __init__(self, df):
        self.df = df

    # Compute single-strategy metrics (kept for backward compatibility)
    def compute(self):
        returns = self.df['strategy_returns'].dropna()

        total_return = self.df['equity_curve'].iloc[-1] / self.df['equity_curve'].iloc[0] - 1
        sharpe = np.sqrt(252) * returns.mean() / returns.std()
        vol = np.sqrt(252) * returns.std()

        return {
            "Total Return": total_return,
            "Sharpe Ratio": sharpe,
            "Annual Volatility": vol,
        }

    # Benchmark-aware summary
    @staticmethod
    def performance_summary(df):
        results = {}

        # Loop over strategy + benchmarks
        for col in ['equity_curve', 'stock_equity', 'spy_equity']:
            returns = df[col].pct_change().dropna()
            total_return = df[col].iloc[-1] / df[col].iloc[0] - 1
            sharpe = (returns.mean() / returns.std()) * np.sqrt(252)
            max_dd = ((df[col] / df[col].cummax()) - 1).min()

            results[col] = {
                'Total Return': total_return,
                'Sharpe': sharpe,
                'Max Drawdown': max_dd
            }

        summary_df = pd.DataFrame(results).T
        summary_df.index = ['Strategy', 'Buy & Hold (Stock)', 'S&P 500 (SPY)']
        return summary_df