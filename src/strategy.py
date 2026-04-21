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
        target_vol=0.02,
        max_leverage=2.0
    ):
        self.data = data.copy()
        self.fast_window = fast_window
        self.slow_window = slow_window
        self.vol_window = vol_window
        self.vol_threshold = vol_threshold
        self.target_vol = target_vol
        self.max_leverage = max_leverage

    def generate_signal(self):
        """
        Returns a pandas Series of signals:
            1  -> buy
            0  -> hold
           -1  -> sell
        Logic:
            - Buy when fast MA > slow MA and volatility is below threshold
            - Sell when fast MA < slow MA or volatility above threshold
        """
        df = self.data.copy()
        # 1. Moving averages
        df["fast_ma"] = df["Close"].rolling(self.fast_window).mean()
        df["slow_ma"] = df["Close"].rolling(self.slow_window).mean()

        # 2. Rolling volatility (std of returns)
        df["returns"] = df["Close"].pct_change()
        df["vol"] = df["returns"].rolling(self.vol_window).std()

        # 3. Signal logic
        signals = pd.Series(0, index=df.index)  # default hold

        buy_condition = (df["fast_ma"] > df["slow_ma"]) & (df["vol"] < self.vol_threshold)
        sell_condition = (df["fast_ma"] < df["slow_ma"]) | (df["vol"] > self.vol_threshold)

        signals[buy_condition] = 1
        signals[sell_condition] = -1

        return signals