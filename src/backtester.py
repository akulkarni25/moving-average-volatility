class Backtester:
    def __init__(self, data, strategy):
        self.data = data
        self.strategy = strategy

    def run(self):
        df = self.strategy.generate_signals()

        df['market_returns'] = df['Close'].pct_change()

        # Position is now scaled (not just 0/1)
        df['strategy_returns'] = df['position'] * df['market_returns']

        df['equity_curve'] = (1 + df['strategy_returns']).cumprod()

        return df