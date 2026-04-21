import pandas as pd
import numpy as np


class MovingAverageVolatilityStrategy:
    def __init__(
        self,
        data: pd.DataFrame,
        fast_window: int = 20,
        slow_window: int = 50,
        vol_window: int = 20,
        vol_threshold: float = 0.01,
        target_vol: float = 0.02,
        max_leverage: float = 2.0
    ):
        self.data = data.copy()
        self.fast_window = fast_window
        self.slow_window = slow_window
        self.vol_window = vol_window
        self.vol_threshold = vol_threshold
        self.target_vol = target_vol
        self.max_leverage = max_leverage

    def generate_signal(self):
        df = self.data.copy()

        df["returns"] = df["Close"].pct_change()
        df["vol"] = df["returns"].rolling(self.vol_window).std()

        df["fast_ma"] = df["Close"].rolling(self.fast_window).mean()
        df["slow_ma"] = df["Close"].rolling(self.slow_window).mean()

        df["trend"] = np.where(df["fast_ma"] > df["slow_ma"], 1, -1)

        momentum = df["trend"] * (df["fast_ma"] / df["slow_ma"] - 1)

        df["weight"] = momentum / (df["vol"] + 1e-8)

        df["weight"] = df["weight"].replace([np.inf, -np.inf], 0).fillna(0)

        return df[["weight"]]