"""Today's rule-based signals, same rules as paper-trader S1 (Donchian breakout) plus a trend regime."""
from __future__ import annotations
import pandas as pd
from .indicators import sma, atr, donchian


def regime(c: pd.Series, n: int = 200) -> pd.Series:
    """'up' above the n-day SMA, 'down' below, 'n/a' until enough history."""
    m = sma(c, n)
    out = pd.Series("n/a", index=c.index, dtype=object)
    out[c > m] = "up"
    out[c < m] = "down"
    return out


def donchian_position(df: pd.DataFrame, n: int = 55, m: int = 20) -> pd.Series:
    """Long-only: enter on close above the prior n-day high, exit on close below the prior m-day low."""
    hi, _ = donchian(df.high, df.low, n)
    _, lo = donchian(df.high, df.low, m)
    pos, cur = [], 0
    for c, h, l in zip(df.close, hi, lo):
        if cur == 0 and pd.notna(h) and c > h:
            cur = 1
        elif cur == 1 and pd.notna(l) and c < l:
            cur = 0
        pos.append(cur)
    return pd.Series(pos, index=df.index, name="position")


def today(df: pd.DataFrame, n: int = 55, m: int = 20, stop_atr: float = 3.0) -> dict:
    pos = donchian_position(df, n, m)
    a = atr(df.high, df.low, df.close).iloc[-1]
    last = df.close.iloc[-1]
    return {
        "date": df.index[-1].date().isoformat(),
        "close": float(last),
        "regime": regime(df.close).iloc[-1],
        "position": "LONG" if pos.iloc[-1] == 1 else "FLAT",
        "stop": float(last - stop_atr * a) if pos.iloc[-1] == 1 else None,
    }
