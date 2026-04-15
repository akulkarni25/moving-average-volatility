import yfinance as yf

class Backtester:
    def __init__(self, data, strategy, initial_capital = 10000):
        self.data = data
        self.strategy = strategy
        self.initial_capital = initial_capital

    def run(self):
        df = self.strategy.generate_signals()

        df['market_returns'] = df['Close'].pct_change()

        # Position is now scaled (not just 0/1)
        df['strategy_returns'] = df['position'] * df['market_returns']

        df['equity_curve'] = (1 + df['strategy_returns']).cumprod() * self.initial_capital

        df = self.compute_benchmarks(df)

        df['strategy_vs_spy'] = df['equity_curve'] / df['spy_equity']
        df['strategy_vs_stock'] = df['equity_curve'] / df['stock_equity']

        return df

    def compute_benchmarks(self, df):
        # --- Buy & Hold (same stock) ---
        df['stock_returns'] = df['Close'].pct_change().fillna(0)
        df['stock_equity'] = (1 + df['stock_returns']).cumprod() * self.initial_capital

        # --- S&P 500 benchmark ---
        spy = yf.download("SPY", start=df.index.min(), end=df.index.max())

        spy['returns'] = spy['Close'].pct_change().fillna(0)
        spy['equity'] = (1 + spy['returns']).cumprod() * self.initial_capital

        # Align dates
        spy = spy.reindex(df.index).ffill()

        df['spy_equity'] = spy['equity']

        return df