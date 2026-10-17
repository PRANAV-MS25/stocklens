import sqlite3
import pandas as pd
import streamlit as st

st.set_page_config(page_title="StockLens - News", layout="wide")
st.title("News")

conn = sqlite3.connect("stocklens.db")
tickers = [r[0] for r in conn.execute("SELECT DISTINCT ticker FROM news ORDER BY ticker")]
if not tickers:
    st.warning("No news yet. Run: python ingest_news.py")
    st.stop()

ticker = st.sidebar.selectbox("Stock", ["All"] + tickers)
query = st.sidebar.text_input("Search headlines")

sql = "SELECT ticker, title, source, published, link FROM news"
where, params = [], []
if ticker != "All":
    where.append("ticker = ?")
    params.append(ticker)
if query.strip():
    where.append("link IN (SELECT link FROM news_fts WHERE news_fts MATCH ?)")
    params.append('"' + query.replace('"', "") + '"')
if where:
    sql += " WHERE " + " AND ".join(where)
sql += " ORDER BY published DESC LIMIT 100"
news = pd.read_sql_query(sql, conn, params=params)

if ticker != "All":
    px = pd.read_sql_query(
        "SELECT date, close FROM prices WHERE ticker = ? ORDER BY date",
        conn, params=(ticker,), parse_dates=["date"],
    ).set_index("date").tail(30)
    st.subheader(f"{ticker}: last 30 trading days")
    st.line_chart(px)
conn.close()

st.subheader(f"{len(news)} headlines")
for r in news.itertuples():
    st.markdown(f"**[{r.title}]({r.link})**  \n{r.source} · {r.published} · `{r.ticker}`")

st.caption("Headlines link to the original publishers. Research tool only, not investment advice.")