import numpy as np
import pandas as pd

TRADING_DAYS = 252


def compute_returns(equity_curve: pd.Series) -> pd.Series:
    return equity_curve.pct_change().dropna()

def total_return(equity_curve):
    return equity_curve.iloc[-1] / equity_curve.iloc[0] - 1


def annualized_return(equity_curve):
    total_ret = total_return(equity_curve)
    n_days = len(equity_curve)
    return (1 + total_ret) ** (TRADING_DAYS / n_days) - 1

def sharpe_ratio(returns, risk_free_rate=0.0):
    excess_returns = returns - risk_free_rate / TRADING_DAYS
    return np.sqrt(TRADING_DAYS) * excess_returns.mean() / excess_returns.std()

def sortino_ratio(returns, risk_free_rate=0.0):
    excess_returns = returns - risk_free_rate / TRADING_DAYS
    downside = returns[returns < 0]
    downside_std = downside.std()
    return np.sqrt(TRADING_DAYS) * excess_returns.mean() / downside_std

def max_drawdown(equity_curve):
    peak = equity_curve.cummax()
    drawdown = (equity_curve - peak) / peak
    return drawdown.min()


def drawdown_duration(equity_curve):
    peak = equity_curve.cummax()
    drawdown = equity_curve < peak

    duration = 0
    max_duration = 0

    for d in drawdown:
        if d:
            duration += 1
            max_duration = max(max_duration, duration)
        else:
            duration = 0

    return max_duration

def calmar_ratio(equity_curve):
    cagr = annualized_return(equity_curve)
    mdd = abs(max_drawdown(equity_curve))
    return cagr / mdd if mdd != 0 else np.nan

def profit_factor(returns):
    gains = returns[returns > 0].sum()
    losses = abs(returns[returns < 0].sum())
    return gains / losses if losses != 0 else np.nan

def performance_report(equity_curve: pd.Series):
    returns = compute_returns(equity_curve)

    report = {
        "Total Return": total_return(equity_curve),
        "Annualized Return": annualized_return(equity_curve),
        "Sharpe Ratio": sharpe_ratio(returns),
        "Sortino Ratio": sortino_ratio(returns),
        "Max Drawdown": max_drawdown(equity_curve),
        "Drawdown Duration": drawdown_duration(equity_curve),
        "Calmar Ratio": calmar_ratio(equity_curve),
        "Profit Factor": profit_factor(returns),
    }

    return pd.Series(report)