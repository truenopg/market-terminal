"""market-terminal: Streamlit dashboard. Run with: streamlit run app.py"""
import plotly.graph_objects as go
import streamlit as st
from terminal.backtest import run, summary
from terminal.data import load
from terminal.indicators import sma
from terminal.signals import donchian_position, today

st.set_page_config(page_title="market-terminal", layout="wide")
st.title("market-terminal")
name = st.sidebar.selectbox("Market", ["BTC", "GOLD"])
n = st.sidebar.slider("Donchian entry (days)", 20, 120, 55)
m = st.sidebar.slider("Donchian exit (days)", 5, 60, 20)
cost = st.sidebar.number_input("Cost per side (bps)", 0.0, 50.0, 5.0)
if st.sidebar.button("Refresh data"):
    load(name, refresh=True)
df = load(name)

t = today(df, n, m)
c1, c2, c3, c4 = st.columns(4)
c1.metric("Close", f"{t['close']:,.2f}", help=t["date"])
c2.metric("Regime (SMA200)", t["regime"])
c3.metric("Donchian position", t["position"])
c4.metric("ATR stop", f"{t['stop']:,.2f}" if t["stop"] else "-")

fig = go.Figure(go.Candlestick(x=df.index, open=df.open, high=df.high, low=df.low, close=df.close, name=name))
for k, col in ((50, "orange"), (200, "royalblue")):
    fig.add_scatter(x=df.index, y=sma(df.close, k), name=f"SMA{k}", line=dict(color=col, width=1))
fig.update_layout(height=520, xaxis_rangeslider_visible=False, margin=dict(l=0, r=0, t=10, b=0))
st.plotly_chart(fig, width='stretch')

st.subheader("Backtest vs buy & hold")
curves = run(df.close, donchian_position(df, n, m), cost)
st.line_chart(curves)
st.dataframe(summary(curves).style.format("{:.1%}"))
st.caption("Educational. Past results, daily bars, no guarantee. Not investment advice.")
