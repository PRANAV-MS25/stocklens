# 🔍 StockLens

A quantitative research assistant and financial analytics engine for 20 large Indian stocks (NSE). It collects daily price action and news headlines, computes trend & volatility metrics, evaluates trade entry signals with profit/tax calculators, and answers questions using grounded LLM synthesis with citations.

> ⚠️ **Disclaimer:** Research tool only. Nothing here is investment advice.

![Ask page](docs/ask.png)

## What it does

- **Dashboard:** Interactive price charts with 20 and 50-day moving averages, return performance, annualized volatility, and volume indicators for 20 NSE stocks.
- **Investment Lens & Signals:** Automated Buy/Hold/Caution signal checks using RSI momentum, moving average crossovers, and valuation P/E metrics. Includes a real-time capital gains profit & tax calculator and a 5-year annualized wealth projection model.
- **Peer Benchmark:** Head-to-head multi-stock comparisons featuring base-100 normalized return growth, Sharpe ratio risk-adjusted evaluations, and cross-stock correlation heatmaps.
- **News:** Aggregates recent headlines per company into a searchable SQLite full-text index (FTS5) displayed alongside price movements.
- **Ask (AI Assistant):** Answers plain language questions by matching stock tickers and relevant headlines, combining computed pandas facts, and asking Gemini to synthesize grounded answers with numbered source citations.

## How it works

```
yfinance (prices) ──► ingest.py ───────┐
├──► SQLite (stocklens.db)
Google News RSS ───► ingest_news.py ───┘          │
▼
Streamlit App (Dashboard, Signals, Benchmark, News)
│
question ──► ticker match + headline search
│
price facts + headlines ──► Gemini API ──► cited answer

```
### Design Principles

- **Deterministic Math:** Returns, annualized volatility, RSI, SMA, and Sharpe ratios are computed strictly using `pandas` and `numpy` rather than relying on LLM estimation.
- **Grounded AI Answers:** Prompts instruct Gemini to answer strictly from provided SQLite context and computed pandas facts, requiring explicit citations and prohibiting financial advice.
- **Untrusted Headline Handling:** News headlines are treated as untrusted data inputs to guard against prompt injection vulnerabilities.
- **Transparent Attribution:** Every retrieved news item retains publisher dates, titles, and direct external links.

## Run it locally

### 1. Set Up Virtual Environment & Dependencies

```
bash
python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On Linux/macOS:
# source .venv/bin/activate

pip install -r requirements.txt
2. Ingest Historical Data
Bash
python ingest.py
python ingest_news.py
3. Set Up Environment Variables
Create a .env file in the project root directory and add your Google Gemini API key:
```
Code snippet
GEMINI_API_KEY=your-gemini-api-key-here
4. Launch the Streamlit App
Bash
python -m streamlit run app.py
Limitations
Data coverage is scoped to 20 key NSE equities and ~2 years of historical daily price bars.

Price feeds rely on yfinance, which may experience minor delays or discrepancies.

The AI context window receives headline titles rather than full article text, so macro explanations may be limited to summary data.

Data ingestion pipeline currently executes via manual script invocation (ingest.py and ingest_news.py).

Roadmap
[x] Investment entry signals & real-time capital gains tax calculator

[x] Multi-stock peer benchmark & Sharpe ratio risk matrix

[ ] Automated daily data refresh via GitHub Actions / Cron

[ ] Automated unit test suite (pytest) for volatility, signal calculations, and ticker resolution

[ ] Backtesting framework evaluating momentum signals against buy-and-hold benchmarks

[ ] Daily summary email/Telegram alerts for ticker price breakouts

Tech Stack
Core & Analytics: Python, Pandas, NumPy, SQLite (FTS5)

Frontend & Visualizations: Streamlit, Plotly Express, Plotly Graph Objects

Data Ingestion: yfinance, Google News RSS

AI & NLP: Google Gemini API (google-genai / google-generativeai)