import pandas as pd
from terminal.indicators import sma, ema, rsi, atr, donchian


def test_sma():
    assert sma(pd.Series([1, 2, 3, 4.0]), 2).tolist()[1:] == [1.5, 2.5, 3.5]


def test_ema_constant_series_is_constant():
    assert (ema(pd.Series([5.0] * 10), 3) == 5.0).all()


def test_rsi_bounds_and_extremes():
    up = rsi(pd.Series(range(1, 40), dtype=float))
    assert up.iloc[-1] == 100
    down = rsi(pd.Series(range(40, 1, -1), dtype=float))
    assert down.iloc[-1] < 1
    mixed = rsi(pd.Series([1, 3, 2, 4, 3, 5, 4, 6, 5, 7.0] * 3))
    assert 0 <= mixed.dropna().min() and mixed.dropna().max() <= 100


def test_atr_constant_range():
    h = pd.Series([11.0] * 30); l = pd.Series([9.0] * 30); c = pd.Series([10.0] * 30)
    assert abs(atr(h, l, c, 5).iloc[-1] - 2.0) < 1e-9


def test_donchian_excludes_today():
    h = pd.Series([1, 2, 3, 10.0]); l = pd.Series([0, 1, 2, 9.0])
    hi, lo = donchian(h, l, 3)
    assert hi.iloc[3] == 3 and lo.iloc[3] == 0  # today's 10 is not in its own channel
