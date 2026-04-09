import matplotlib.pyplot as plt

class Visualizer:
    def __init__(self, df):
        self.df = df

    def plot(self):
        fig, axs = plt.subplots(4, 1, figsize=(12, 12), sharex=True)

        # Price + MAs
        axs[0].plot(self.df['Close'], label='Price')
        axs[0].plot(self.df['fast_ma'], label='Fast MA')
        axs[0].plot(self.df['slow_ma'], label='Slow MA')
        axs[0].legend()
        axs[0].set_title("Price & Moving Averages")

        # Volatility
        axs[1].plot(self.df['volatility'], label='Volatility', color='orange')
        axs[1].set_title("Volatility")

        # Position size
        axs[2].plot(self.df['position'], label='Position Size', color='purple')
        axs[2].set_title("Position Sizing")

        # Equity curve
        axs[3].plot(self.df['equity_curve'], label='Equity Curve', color='green')
        axs[3].set_title("Strategy Performance")

        plt.tight_layout()
        plt.show()