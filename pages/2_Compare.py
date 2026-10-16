import sqlite3
import pandas as pd
import streamlit as st

st.set_page_config(page_title="StockLens - Compare", layout="wide")
st.title("Compare stocks")


@st.cache_data
def load_all():
    conn = sqlite3.connect("stocklens.db")
    df = pd.read_sql_query(
        "SELECT ticker, date, close FROM prices ORDER BY date",
        conn, parse_dates=["date"],
    )
    conn.close()
    return df.pivot(index="date", columns="ticker", values="close")


prices = load_all()
chosen = st.sidebar.multiselect(
    "Stocks", list(prices.columns), default=["TCS.NS", "INFY.NS"]
)
days = st.sidebar.select_slider(
    "Period (trading days)", options=[30, 90, 180, 365, 497], value=365
)

if len(chosen) < 2:
    st.info("Pick at least two stocks in the sidebar.")
    st.stop()

view = prices[chosen].tail(days).dropna()
rebased = view / view.iloc[0] * 100
returns = view.iloc[-1] / view.iloc[0] - 1

best, worst = returns.idxmax(), returns.idxmin()
c1, c2 = st.columns(2)
c1.metric("Best performer", best, f"{returns[best]:.1%}")
c2.metric("Worst performer", worst, f"{returns[worst]:.1%}")

st.subheader("Price rebased to 100 at the start")
st.line_chart(rebased)

st.subheader("Correlation of daily returns")
st.dataframe(view.pct_change().corr().round(2))

st.caption("Research tool only, not investment advice.")