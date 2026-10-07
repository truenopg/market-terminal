"""Tiny vectorised backtest for a 0/1 position series, compared with buy & hold."""
from __future__ import annotations
import pandas as pd


def run(close: pd.Series, position: pd.Series, cost_bps: float = 5.0) -> pd.DataFrame:
    """Position decided at the close of day t is held from t+1 (shift(1)), so no lookahead.
    Cost is charged on every change of position, in bps of traded notional."""
    r = close.pct_change().fillna(0.0)
    pos = position.shift(1).fillna(0.0)
    cost = position.diff().abs().fillna(position.abs()).shift(1).fillna(0.0) * cost_bps / 1e4
    strat = pos * r - cost
    return pd.DataFrame({"strategy": (1 + strat).cumprod(), "buy_hold": (1 + r).cumprod()})


def max_drawdown(equity: pd.Series) -> float:
    return float((equity / equity.cummax() - 1).min())


def summary(curves: pd.DataFrame, periods: int = 365) -> pd.DataFrame:
    # Calendar years when the index holds dates (gold trades ~252 bars/year, BTC ~365),
    # otherwise fall back to a fixed bars-per-year count.
    if isinstance(curves.index, pd.DatetimeIndex) and len(curves) > 1:
        yrs = (curves.index[-1] - curves.index[0]).days / 365.25
    else:
        yrs = len(curves) / periods
    rows = {}
    for k in curves:
        e = curves[k]
        rows[k] = {"total_return": e.iloc[-1] - 1, "cagr": e.iloc[-1] ** (1 / yrs) - 1 if yrs > 0 else 0.0,
                   "max_drawdown": max_drawdown(e)}
    return pd.DataFrame(rows).T
