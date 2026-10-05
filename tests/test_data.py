import pandas as pd
from terminal.data import parse_coinbase, clean


def test_parse_coinbase_orders_columns_and_sorts():
    rows = [[1700086400, 9, 12, 10, 11, 5.0], [1700000000, 8, 11, 9, 10, 4.0]]  # newest first
    df = parse_coinbase(rows)
    assert list(df.columns) == ["open", "high", "low", "close", "volume"]
    assert df.index.is_monotonic_increasing
    assert df.iloc[0].open == 9 and df.iloc[0].low == 8 and df.iloc[0].close == 10


def test_clean_drops_bad_rows_and_duplicates():
    idx = pd.to_datetime(["2024-01-02", "2024-01-01", "2024-01-02", "2024-01-03"])
    df = pd.DataFrame({"open": [1, 1, 2, 0], "high": [2, 2, 3, 1], "low": [1, 1, 1, 0],
                       "close": [1.5, 1.5, 2, 0], "volume": [1, 1, 1, 1]}, index=idx)
    out = clean(df)
    assert list(out.index) == list(pd.to_datetime(["2024-01-01", "2024-01-02"]))
    assert out.loc["2024-01-02", "open"] == 2  # keeps the last duplicate
