import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from backtester import load_data

# -------------------------------
# 1. Load Data
# -------------------------------
tickers = ['TSLA', 'NVDA']
data = load_data(tickers=tickers, start='2020-01-01')

# -------------------------------
# 2. Strategy parameters
# -------------------------------
short_window = 20
long_window = 50

# Dictionary to hold results
results = {}

for ticker in tickers:
    price = data[ticker]

    # Compute moving averages
    ma_short = price.rolling(window=short_window).mean()
    ma_long = price.rolling(window=long_window).mean()

    # Generate signals: 1 = long, -1 = short
    signal = pd.Series(np.where(ma_short > ma_long, 1, -1), index=price.index)
    position = np.diff(signal, prepend=0)  # identifies buy/sell points

    # Compute cumulative P&L
    returns = price.pct_change() * signal.shift(1)
    cumulative_pnl = (1 + returns).cumprod()

    # Store results
    results[ticker] = {
        'price': price,
        'ma_short': ma_short,
        'ma_long': ma_long,
        'signal': signal,
        'position': position,
        'cumulative_pnl': cumulative_pnl
    }

# -------------------------------
# 3. Plot Price + Moving Averages
# -------------------------------
for ticker in tickers:
    r = results[ticker]
    plt.figure(figsize=(14, 6))
    plt.plot(r['price'], label=f'{ticker} Price', color='black')
    plt.plot(r['ma_short'], label=f'{short_window}-day MA', color='blue')
    plt.plot(r['ma_long'], label=f'{long_window}-day MA', color='red')
    plt.title(f'{ticker} Price with Moving Averages')
    plt.legend()
    plt.show()

# -------------------------------
# 4. Plot Signals on Price Chart
# -------------------------------
for ticker in tickers:
    r = results[ticker]
    plt.figure(figsize=(14, 6))
    plt.plot(r['price'], label=f'{ticker} Price', color='black')
    plt.plot(r['ma_short'], label=f'{short_window}-day MA', color='blue')
    plt.plot(r['ma_long'], label=f'{long_window}-day MA', color='red')

    # Buy signals (position change = 2)
    plt.plot(r['price'].index[r['position'] == 2],
             r['price'][r['position'] == 2],
             '^', markersize=10, color='green', label='Buy Signal')

    # Sell signals (position change = -2)
    plt.plot(r['price'].index[r['position'] == -2],
             r['price'][r['position'] == -2],
             'v', markersize=10, color='red', label='Sell Signal')

    plt.title(f'{ticker} Trading Signals')
    plt.legend()
    plt.show()

# -------------------------------
# 5. Plot Cumulative P&L
# -------------------------------
for ticker in tickers:
    r = results[ticker]
    plt.figure(figsize=(14, 6))
    plt.plot(r['cumulative_pnl'], label=f'{ticker} Cumulative P&L', color='purple')
    plt.title(f'{ticker} Moving Average Strategy Cumulative P&L')
    plt.xlabel('Date')
    plt.ylabel('Portfolio Value')
    plt.legend()
    plt.show()