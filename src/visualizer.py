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
        axs[3].plot(self.df['equity_curve'], label='Strategy', color='green')
        axs[3].plot(self.df['stock_equity'], label='Buy & Hold (Stock)', linestyle='--', color='blue')
        axs[3].plot(self.df['spy_equity'], label='S&P 500 (SPY)', linestyle=':', color='red')
        axs[3].set_title("Strategy vs Benchmarks")
        axs[3].legend()

        plt.tight_layout()
        plt.show()

    @staticmethod
    def plot_equity_curves(df):
        plt.figure(figsize=(12, 6))

        plt.plot(df.index, df['equity_curve'], label='Strategy', linewidth=2)
        plt.plot(df.index, df['stock_equity'], label='Buy & Hold (Stock)', linestyle='--')
        plt.plot(df.index, df['spy_equity'], label='S&P 500 (SPY)', linestyle=':')

        plt.title("Strategy vs Benchmarks")
        plt.legend()
        plt.grid()
        plt.show()