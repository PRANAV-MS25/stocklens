import sqlite3
import time
import xml.etree.ElementTree as ET
from email.utils import parsedate_to_datetime
from urllib.parse import quote_plus

import requests

COMPANIES = {
    "TCS.NS": "Tata Consultancy Services",
    "INFY.NS": "Infosys",
    "WIPRO.NS": "Wipro",
    "HCLTECH.NS": "HCL Technologies",
    "RELIANCE.NS": "Reliance Industries",
    "HDFCBANK.NS": "HDFC Bank",
    "ICICIBANK.NS": "ICICI Bank",
    "SBIN.NS": "State Bank of India",
    "ITC.NS": "ITC Limited",
    "LT.NS": "Larsen & Toubro",
    "BHARTIARTL.NS": "Bharti Airtel",
    "HINDUNILVR.NS": "Hindustan Unilever",
    "KOTAKBANK.NS": "Kotak Mahindra Bank",
    "AXISBANK.NS": "Axis Bank",
    "MARUTI.NS": "Maruti Suzuki",
    "SUNPHARMA.NS": "Sun Pharma",
    "BAJFINANCE.NS": "Bajaj Finance",
    "TITAN.NS": "Titan Company",
    "ASIANPAINT.NS": "Asian Paints",
    "ADANIENT.NS": "Adani Enterprises",
}

conn = sqlite3.connect("stocklens.db")
conn.execute(
    """CREATE TABLE IF NOT EXISTS news (
        ticker TEXT, title TEXT, link TEXT, source TEXT, published TEXT,
        PRIMARY KEY (ticker, link))"""
)
conn.execute(
    "CREATE VIRTUAL TABLE IF NOT EXISTS news_fts USING fts5("
    "title, ticker UNINDEXED, link UNINDEXED)"
)

for ticker, name in COMPANIES.items():
    q = quote_plus(f"{name} share when:30d")
    url = f"https://news.google.com/rss/search?q={q}&hl=en-IN&gl=IN&ceid=IN:en"
    try:
        resp = requests.get(url, timeout=15, headers={"User-Agent": "Mozilla/5.0"})
        root = ET.fromstring(resp.content)
    except Exception as e:
        print(f"{ticker}: failed ({e})")
        continue

    added = 0
    for item in root.iter("item"):
        title = item.findtext("title") or ""
        link = item.findtext("link") or ""
        source = item.findtext("source") or ""
        pub = item.findtext("pubDate")
        published = parsedate_to_datetime(pub).strftime("%Y-%m-%d %H:%M") if pub else ""
        cur = conn.execute(
            "INSERT OR IGNORE INTO news VALUES (?,?,?,?,?)",
            (ticker, title, link, source, published),
        )
        if cur.rowcount:
            conn.execute(
                "INSERT INTO news_fts (title, ticker, link) VALUES (?,?,?)",
                (title, ticker, link),
            )
            added += 1
    conn.commit()
    print(f"{ticker}: {added} new headlines")
    time.sleep(1)

conn.close()