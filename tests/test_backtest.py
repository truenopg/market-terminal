import pandas as pd
from terminal.backtest import run, max_drawdown, summary


def s(v):
    return pd.Series(v, dtype=float, index=pd.date_range("2024-01-01", periods=len(v)))


def test_always_flat_equity_is_one():
    out = run(s([10, 11, 12, 13]), s([0, 0, 0, 0]))
    assert (out.strategy == 1).all()


def test_no_lookahead_signal_acts_next_day():
    # price jumps on day 2; a position set at close of day 2 must NOT capture that jump
    out = run(s([10, 10, 20, 20]), s([0, 0, 1, 1]), cost_bps=0)
    assert out.strategy.iloc[-1] == 1.0
    # a position set the day before the jump does capture it
    out = run(s([10, 10, 20, 20]), s([0, 1, 1, 1]), cost_bps=0)
    assert out.strategy.iloc[-1] == 2.0


def test_costs_reduce_equity():
    c, p = s([10, 10, 10, 10]), s([0, 1, 0, 0])
    assert run(c, p, 0).strategy.iloc[-1] == 1.0
    assert run(c, p, 50).strategy.iloc[-1] < 1.0


def test_max_drawdown():
    assert abs(max_drawdown(s([1, 2, 1, 3])) - (-0.5)) < 1e-12


def test_summary_shape():
    t = summary(run(s([10, 11, 12, 13]), s([1, 1, 1, 1])))
    assert set(t.index) == {"strategy", "buy_hold"} and "max_drawdown" in t.columns
