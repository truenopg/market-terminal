"""Data layer: daily OHLCV for BTC (Coinbase) and gold futures (Yahoo GC=F), cached as CSV."""
from __future__ import annotations
import json, urllib.request
from datetime import datetime, timezone
from pathlib import Path
import pandas as pd

CACHE = Path(".cache")
COLS = ["open", "high", "low", "close", "volume"]


def parse_coinbase(rows: list[list]) -> pd.DataFrame:
    """Coinbase candles are [time, low, high, open, close, volume], newest first."""
    df = pd.DataFrame(rows, columns=["time", "low", "high", "open", "close", "volume"])
    df.index = pd.to_datetime(df.pop("time"), unit="s", utc=True).dt.tz_localize(None).dt.normalize()
    df.index.name = "date"
    return df[COLS].astype(float).sort_index()


def fetch_coinbase(product: str = "BTC-USD", days: int = 1500) -> pd.DataFrame:
    """Coinbase returns at most 300 candles per call, so page backwards."""
    end = datetime.now(timezone.utc)
    parts = []
    while days > 0:
        n = min(300, days)
        start = end - pd.Timedelta(days=n)
        url = (f"https://api.exchange.coinbase.com/products/{product}/candles?granularity=86400"
               f"&start={start.isoformat()}&end={end.isoformat()}")
        req = urllib.request.Request(url, headers={"User-Agent": "market-terminal"})
        rows = json.load(urllib.request.urlopen(req, timeout=30))
        if not rows:
            break
        parts.append(parse_coinbase(rows))
        end, days = start, days - n
    df = pd.concat(parts).sort_index()
    return df[~df.index.duplicated()]


def fetch_yahoo(symbol: str = "GC=F", start: str = "2015-01-01") -> pd.DataFrame:
    import yfinance as yf
    d = yf.download(symbol, start=start, progress=False, auto_adjust=True)
    d.columns = [c[0].lower() if isinstance(c, tuple) else c.lower() for c in d.columns]
    d.index.name = "date"
    return d[COLS].dropna()


def clean(df: pd.DataFrame) -> pd.DataFrame:
    """Sort, drop duplicate dates and rows with non-positive or inconsistent prices."""
    df = df.sort_index()
    df = df[~df.index.duplicated(keep="last")]
    ok = (df[["open", "high", "low", "close"]] > 0).all(axis=1) & (df.high >= df.low)
    return df[ok]


def load(name: str, refresh: bool = False) -> pd.DataFrame:
    CACHE.mkdir(exist_ok=True)
    f = CACHE / f"{name}.csv"
    if f.exists() and not refresh:
        return pd.read_csv(f, index_col="date", parse_dates=True)
    df = clean(fetch_coinbase() if name == "BTC" else fetch_yahoo())
    df.to_csv(f)
    return df
