# market-terminal

A small Streamlit dashboard for daily BTC and gold data: price, trend,
volatility and a long-only Donchian breakout, with a backtest beside buy & hold.
No paid feeds, broker connection or live orders.

Companion to [backtest-engine](https://github.com/truenopg/backtest-engine) and
[paper-trader](https://github.com/truenopg/paper-trader). This dashboard computes
its own curves from the selected data rather than importing saved results.

## Run

Use Python 3.10 or newer. From the repository root:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

The first launch downloads data and writes `.cache/BTC.csv` or
`.cache/GOLD.csv`. Later launches reuse those files. Select **Refresh data**
to download again; the app does not refresh automatically. Internet access
is needed for the first download and each refresh.

## Reading the dashboard

- **Market:** BTC-USD daily Coinbase candles or Yahoo's GC=F gold futures series.
  The gold series is not spot gold or a broker's XAUUSD CFD.
- **Entry / exit:** default 55-day entry and 20-day exit. Enter long when the
  close exceeds the previous entry-window high; exit when the close falls
  below the previous exit-window low. Otherwise hold the existing position.
- **Regime:** close above or below SMA200. This is a label, not an entry filter.
- **Donchian position:** LONG or FLAT after processing the latest available bar,
  not a new order instruction. Check the date shown in the Close tooltip.
- **ATR stop:** latest close minus three times ATR(14), shown only while LONG.
  It is an indicative level, not a stop enforced by the backtest.
- **Backtest:** unit starting capital, no leverage, strategy versus buy & hold.
  The selected cost is charged per side on position changes. Buy & hold has
  no transaction costs in this simple comparison.

## Assumptions and limits

The backtest shifts the close-based position by one bar before applying
close-to-close returns. It is an illustrative return calculation, not an
execution simulator: no next-open fills, intraday stops, financing, spread
model or futures roll costs. CAGR is computed over calendar time
between the first and last date, so gold and BTC are annualized consistently.
Total return and drawdown do not use that annualization assumption.

A candle dated today (UTC) is dropped when data is first downloaded, since it
is still forming; an already cached file is not re-checked until you refresh.
Cached data can be stale,
provider requests can fail, and the two markets have different calendars and
history lengths. Changing lookbacks on the same sample is not an
out-of-sample test. Nothing here establishes a profitable trading strategy.

## Tests

From the repository root, after installing the requirements:

```bash
(cd tests && PYTHONPATH=.. ../.venv/bin/python -m pytest -q)
```

17 tests currently cover candle parsing and cleaning, indicators, signals,
lagged returns and costs, and a Streamlit smoke test using synthetic cached
data. Tests do not require a market-data download.

## Roadmap

- [x] BTC and gold daily data with local CSV cache
- [x] SMA, EMA, RSI, ATR and Donchian indicators
- [x] Candlestick chart with SMA50/200 overlays
- [x] Donchian position and indicative ATR stop
- [x] Backtest curves and summary table
- [x] Unit tests and cached-data app smoke test
- [ ] CI
- [ ] Multi-market screener and correlation view
- [ ] Calendar-aware annualization and clearer data freshness

## License

MIT - see [LICENSE](LICENSE).
