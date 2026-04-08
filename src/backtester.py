import yfinance as yf
import pandas as pd

def load_data(tickers=['TSLA', 'NVDA'], start='2020-01-01', end=None):
    df = yf.download(tickers, start=start, end=end, auto_adjust=True, progress=False)
    if isinstance(df.columns, pd.MultiIndex):
        df = df.xs('Close', axis=1, level=0)
    else:
        ticker = tickers[0]
        df = df[['Close']].rename(columns={'Close': ticker})
    df.dropna(inplace=True)
    return df