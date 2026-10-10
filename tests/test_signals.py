import pandas as pd
from terminal.signals import regime, donchian_position, today


def frame(closes):
    c = pd.Series(closes, dtype=float, index=pd.date_range("2024-01-01", periods=len(closes)))
    return pd.DataFrame({"open": c, "high": c + 0.5, "low": c - 0.5, "close": c, "volume": 1.0})


def test_regime_up_down_and_warmup():
    r = regime(pd.Series(range(1, 301), dtype=float))
    assert r.iloc[10] == "n/a" and r.iloc[-1] == "up"
    assert regime(pd.Series(range(300, 0, -1), dtype=float)).iloc[-1] == "down"


def test_breakout_enters_and_exits():
    df = frame([10] * 10 + [20] * 3 + [5] * 3)
    pos = donchian_position(df, n=5, m=3)
    assert pos.iloc[9] == 0
    assert pos.iloc[10] == 1       # close 20 above prior 5-day high
    assert pos.iloc[-1] == 0       # close 5 below prior 3-day low


def test_today_flat_has_no_stop():
    out = today(frame([10] * 30))
    assert out["position"] == "FLAT" and out["stop"] is None


def test_today_long_stop_below_close():
    out = today(frame([10] * 60 + [30]), n=20, m=10)
    assert out["position"] == "LONG" and out["stop"] < out["close"]


def test_today_stop_is_close_minus_atr_multiple():
    from terminal.indicators import atr
    df = frame([10] * 60 + [30])
    out = today(df, n=20, m=10, stop_atr=2.0)
    a = atr(df.high, df.low, df.close).iloc[-1]
    assert abs(out["stop"] - (30 - 2.0 * a)) < 1e-9
