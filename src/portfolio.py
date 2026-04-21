# portfolio.py

import pandas as pd

# Global portfolio state
portfolio = {
    "positions": {}  # dynamically filled by initialize_positions
}


def initialize_positions(data_dict, initial_capital=5000):
    """
    Initialize each ticker with equal initial capital.
    """
    portfolio["positions"] = {}
    for ticker, df in data_dict.items():
        price = df["Close"].iloc[0].values[0]
        print(price)
        shares = initial_capital / price
        portfolio["positions"][ticker] = {"shares": shares}


def rebalance(date, data_dict, signals_dict):
    """
    Rotate capital between tickers according to signals.
    Rules:
        - Sell signal: move entire position to other tickers with no sell signal
        - Buy signal: invest available capital if currently not invested
        - Hold signal: do nothing
    Assumes 2 tickers for now.
    """
    tickers = list(data_dict.keys())
    if len(tickers) != 2:
        raise ValueError("Currently only supports 2 tickers")

    t1, t2 = tickers
    pos1 = portfolio["positions"][t1]
    pos2 = portfolio["positions"][t2]
    pos1_shares = pos1["shares"]
    print(pos1_shares)
    pos2_shares = pos2["shares"]
    print(pos2_shares)

    price1 = data_dict[t1].loc[date, "Close"]
    price2 = data_dict[t2].loc[date, "Close"]

    val1 = pos1_shares * price1
    val2 = pos2_shares * price2

    sig1 = signals_dict[t1].loc[date]
    sig2 = signals_dict[t2].loc[date]

    # Rotation logic
    if sig1 == -1 and pos1_shares > 0:
        # Sell t1 → move to t2
        capital = val1
        pos1["shares"] = 0
        pos2["shares"] += capital / price2

    elif sig2 == -1 and pos2["shares"] > 0.0:
        # Sell t2 → move to t1
        capital = val2
        pos2["shares"] = 0
        pos1["shares"] += capital / price1

    elif sig1 == 1 and pos1["shares"] == 0.0 and pos2["shares"] > 0.0:
        # Buy t1 → use t2 capital
        capital = val2
        pos2["shares"] = 0
        pos1["shares"] += capital / price1

    elif sig2 == 1 and pos2["shares"] == 0 and pos1["shares"] > 0:
        # Buy t2 → use t1 capital
        capital = val1
        pos1["shares"] = 0
        pos2["shares"] += capital / price2


def compute_portfolio_value(date, data_dict):
    """
    Returns total portfolio value at a given date
    """
    total = 0
    for ticker, df in data_dict.items():
        price = df.loc[date, "Close"]
        shares = portfolio["positions"][ticker]["shares"]
        total += shares * price
    return total