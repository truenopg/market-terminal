from streamlit.testing.v1 import AppTest
import pandas as pd


def test_app_runs_with_cached_data(tmp_path, monkeypatch):
    import terminal.data as data
    idx = pd.date_range("2023-01-01", periods=400)
    c = pd.Series(range(100, 500), dtype=float, index=idx)
    df = pd.DataFrame({"open": c, "high": c + 1, "low": c - 1, "close": c, "volume": 1.0})
    df.index.name = "date"
    monkeypatch.setattr(data, "CACHE", tmp_path)
    df.to_csv(tmp_path / "BTC.csv")
    at = AppTest.from_file("../app.py", default_timeout=60).run()
    assert not at.exception
    assert [m.label for m in at.metric][:2] == ["Close", "Regime (SMA200)"]
