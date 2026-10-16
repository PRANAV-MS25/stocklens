import sqlite3
import pandas as pd
import streamlit as st

st.set_page_config(page_title="StockLens", layout="wide")
st.title("StockLens")


@st.cache_data
def load_prices(ticker):
    conn = sqlite3.connect("stocklens.db")
    df = pd.read_sql_query(
        "SELECT date, close, volume FROM prices WHERE ticker = ? ORDER BY date",
        conn, params=(ticker,), parse_dates=["date"],
    )
    conn.close()
    return df.set_index("date")


conn = sqlite3.connect("stocklens.db")
tickers = [r[0] for r in conn.execute("SELECT DISTINCT ticker FROM prices ORDER BY ticker")]
conn.close()

ticker = st.sidebar.selectbox("Stock", tickers)
days = st.sidebar.select_slider("Period (trading days)", options=[30, 90, 180, 365, 497], value=365)

df = load_prices(ticker)
df["MA20"] = df["close"].rolling(20).mean()
df["MA50"] = df["close"].rolling(50).mean()
view = df.tail(days)

ret = view["close"].iloc[-1] / view["close"].iloc[0] - 1
vol = df["close"].pct_change().tail(days).std() * (252 ** 0.5)

c1, c2, c3 = st.columns(3)
c1.metric("Last close", f"₹{view['close'].iloc[-1]:,.2f}")
c2.metric(f"Return ({days} days)", f"{ret:.1%}")
c3.metric("Annualized volatility", f"{vol:.1%}")

st.subheader("Price with 20 and 50-day moving averages")
st.line_chart(view[["close", "MA20", "MA50"]])
st.subheader("Volume")
st.bar_chart(view["volume"])

st.caption("Research tool only, not investment advice. Data via yfinance and may be delayed.")