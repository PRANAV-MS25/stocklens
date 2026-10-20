# 📈 StockLens — Quantitative Market Assistant & AI Research Engine

StockLens is a full-stack financial analytics and quantitative research platform built for Indian Stock Exchange (NSE) equities. It bridges the gap between raw market data and actionable investment decisions by combining real-time price ingestion, automated technical indicators, multi-stock risk benchmarking, dynamic profit/tax calculators, and a grounded LLM research assistant.

> ⚠️ **Disclaimer:** Research tool only. Nothing here constitutes professional financial or investment advice.

---

## 📁 Project Structure

stocklens/
├── pages/                          # Streamlit multi-page interface
│   ├── 02_Investment_Lens.py       # Buy/Hold signal generator & profit/tax calculator
│   ├── 3_News.py                   # Google News RSS aggregator & sentiment viewer
│   ├── 4_Ask.py                    # Grounded AI research assistant (Gemini API)
│   └── 5_Peer_Benchmark.py         # Multi-stock risk/return matrix & correlation heatmap
├── tests/                          # Automated test suite
│   └── test_signals.py             # Unit tests for RSI, momentum, and tax calculations
├── docs/                           # Documentation assets & screenshots
│   └── ask.png                     # AI assistant UI preview
├── .env                            # Environment variables (API keys)
├── app.py                          # Main Streamlit dashboard application
├── core.py                         # Quantitative analysis core (returns, volatility, helpers)
├── ingest.py                       # yfinance daily price ingestion pipeline
├── ingest_news.py                  # Google News RSS headline scraper
├── notify_test.py                  # Automated alert notification script
├── requirements.txt                # Project dependencies
└── stocklens.db                    # SQLite database (Prices, FTS5 News index)

---

## 🗄️ Database Schema & Architecture

### `prices` (SQLite)
| Field | Type | Description |
|-------|------|---|
| ticker | VARCHAR | NSE Stock Symbol (e.g., RELIANCE.NS) |
| date | DATETIME | Trading session date |
| Open / High / Low / Close | DECIMAL | Daily price action |
| Volume | BIGINT | Traded volume |

### `news` (SQLite FTS5 Full-Text Index)
| Field | Type | Description |
|-------|------|---|
| ticker | VARCHAR | Associated stock symbol |
| headline | TEXT | News article title |
| date | DATETIME | Publication timestamp |
| url | TEXT | Direct link to publisher source |

---

## ⚙️ Setup & Installation Instructions

### 1. Prerequisites
```
bash
Python 3.10+
pip
```
git clone [https://github.com/PRANAV-MS25/stocklens.git](https://github.com/PRANAV-MS25/stocklens.git)
cd stocklens
```
