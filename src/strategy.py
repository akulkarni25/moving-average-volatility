import pandas as pd
import numpy as np

class MovingAverageVolatilityStrategy:
    def __init__(
        self,
        data,
        fast_window=20,
        slow_window=50,
        vol_window=20,
        vol_threshold=0.01,
        target_vol=0.02,   # target portfolio volatility
        max_leverage=2.0   # cap position size
    ):
        self.data = data.copy()
        self.fast_window = fast_window
        self.slow_window = slow_window
        self.vol_window = vol_window
        self.vol_threshold = vol_threshold
        self.target_vol = target_vol
        self.max_leverage = max_leverage

    def generate_signals(self):
        df = self.data.copy()

        # Moving averages
        df['fast_ma'] = df['Close'].rolling(self.fast_window).mean()
        df['slow_ma'] = df['Close'].rolling(self.slow_window).mean()

        # Returns + volatility
        df['returns'] = df['Close'].pct_change()
        df['volatility'] = df['returns'].rolling(self.vol_window).std()

        # Base signal (trend + volatility filter)
        df['signal'] = 0

        long_condition = (
            (df['fast_ma'] > df['slow_ma']) &
            (df['volatility'] > self.vol_threshold)
        )

        df.loc[long_condition, 'signal'] = 1

        # --- NEW: Position sizing ---
        # Avoid division by zero
        df['volatility'] = df['volatility'].replace(0, np.nan)

        # Position size = target_vol / actual_vol
        df['position_size'] = self.target_vol / df['volatility']

        # Cap leverage
        df['position_size'] = df['position_size'].clip(upper=self.max_leverage)

        # Apply signal (only take position when signal = 1)
        df['position'] = df['signal'] * df['position_size']

        # Shift to avoid lookahead bias
        df['position'] = df['position'].shift(1).fillna(0)

        return df