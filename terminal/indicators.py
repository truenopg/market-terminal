"""Indicators on a close/high/low Series. Same definitions as backtest-engine."""
import pandas as pd


def sma(c: pd.Series, n: int) -> pd.Series:
    return c.rolling(n).mean()


def ema(c: pd.Series, n: int) -> pd.Series:
    return c.ewm(span=n, adjust=False).mean()


def rsi(c: pd.Series, n: int = 14) -> pd.Series:
    """Wilder RSI. A series with no losses returns 100."""
    d = c.diff()
    up = d.clip(lower=0).ewm(alpha=1 / n, adjust=False).mean()
    dn = (-d.clip(upper=0)).ewm(alpha=1 / n, adjust=False).mean()
    out = 100 - 100 / (1 + up / dn)
    return out.where(dn != 0, 100.0).where(d.notna())


def atr(h: pd.Series, l: pd.Series, c: pd.Series, n: int = 14) -> pd.Series:
    pc = c.shift(1)
    tr = pd.concat([h - l, (h - pc).abs(), (l - pc).abs()], axis=1).max(axis=1)
    return tr.ewm(alpha=1 / n, adjust=False).mean()


def donchian(h: pd.Series, l: pd.Series, n: int = 20):
    """Channel of the previous n bars (excludes today, so a breakout is detectable)."""
    return h.rolling(n).max().shift(1), l.rolling(n).min().shift(1)
