import sqlite3
import yfinance as yf

TICKERS = [
    "TCS.NS", "INFY.NS", "WIPRO.NS", "HCLTECH.NS", "RELIANCE.NS",
    "HDFCBANK.NS", "ICICIBANK.NS", "SBIN.NS", "ITC.NS", "LT.NS",
    "BHARTIARTL.NS", "HINDUNILVR.NS", "KOTAKBANK.NS", "AXISBANK.NS",
    "MARUTI.NS", "SUNPHARMA.NS", "BAJFINANCE.NS", "TITAN.NS",
    "ASIANPAINT.NS", "ADANIENT.NS",
]

conn = sqlite3.connect("stocklens.db")
conn.execute(
    """CREATE TABLE IF NOT EXISTS prices (
        ticker TEXT, date TEXT, open REAL, high REAL,
        low REAL, close REAL, volume INTEGER,
        PRIMARY KEY (ticker, date))"""
)

for t in TICKERS:
    df = yf.Ticker(t).history(period="2y").reset_index()
    if df.empty:
        print(f"{t}: no data")
        continue
    rows = [
        (t, r.Date.strftime("%Y-%m-%d"), r.Open, r.High, r.Low, r.Close, int(r.Volume))
        for r in df.itertuples()
    ]
    conn.executemany("INSERT OR REPLACE INTO prices VALUES (?,?,?,?,?,?,?)", rows)
    conn.commit()
    print(f"{t}: {len(rows)} rows")

conn.close()