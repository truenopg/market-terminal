# market-terminal

A small Streamlit dashboard for looking at markets the way a systematic
trader does: price, trend, volatility and the signals of a few rule-based
strategies, on free real data, with no paid feeds.

Companion to [backtest-engine](https://github.com/truenopg/backtest-engine) and
[paper-trader](https://github.com/truenopg/paper-trader): same indicators,
same strategy rules, so what you see on the chart is what was backtested.

## Status

Work in progress, built in small steps. See the roadmap.

## Roadmap

- [x] Data layer: BTC (Coinbase) and gold (Yahoo GC=F) daily bars, cached locally
- [x] Indicators: SMA, EMA, RSI, ATR, Donchian channels
- [ ] Price chart with overlays and the current trend regime (above/below SMA200)
- [x] Strategy signals (panel UI pending): today's signal for each rule-based strategy and its stop distance
- [x] Backtest engine (view pending): equity curve vs buy & hold from paper-trader results
- [ ] Tests and CI

## Run (once the app lands)

```bash
pip install -r requirements.txt
streamlit run app.py
```

## License

MIT - see [LICENSE](LICENSE).
