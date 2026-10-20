# 📈 StockLens

A quantitative research assistant and financial analytics platform for Indian Stock Exchange (NSE) equities. StockLens combines real-time price ingestion, automated technical indicators, multi-stock risk benchmarking, dynamic profit/tax calculators, and a grounded LLM research assistant.

> ⚠️ **Disclaimer:** Research tool only. Nothing here constitutes professional financial or investment advice.

---

## 🚀 Key Features

- **📊 Dashboard:** Interactive price charts with 20/50-day moving averages, returns, volatility, and volume indicators.
- **🎯 Dynamic Investment Lens:** Time-frame dependent Buy/Hold/Caution signals (RSI, moving averages, P/E) that update instantly when switching durations (`3mo`, `1y`, `2y`, `5y`).
- **💰 Profit & Tax Calculator:** Real-time trade ROI simulation, gross/net profit breakdown, Short-Term Capital Gains (STCG) tax adjustment, and 5-year wealth compounding projections.
- **⚖️ Peer Benchmark Matrix:** Base-100 normalized performance trajectory, Sharpe Ratio risk-adjusted returns, and cross-asset correlation heatmaps.
- **🤖 Grounded AI Copilot:** Natural language Q&A backed by the Google Gemini API, synthesizing pandas price facts and SQLite news records with numbered source citations.

``

## 📁 Project Structure

stocklens/
├── pages/                          # Streamlit multi-page interface
│   ├── 02_Investment_Lens.py       # Signal generator & profit/tax calculator
│   ├── 3_News.py                   # Google News RSS aggregator & viewer
│   ├── 4_Ask.py                    # Grounded AI research assistant (Gemini)
│   └── 5_Peer_Benchmark.py         # Multi-stock risk/return matrix & heatmap
├── tests/                          # Automated unit test suite
│   └── test_signals.py             # Tests for RSI, momentum, and tax logic
├── app.py                          # Main Streamlit dashboard application
├── core.py                         # Quantitative analysis core functions
├── ingest.py                       # yfinance daily price ingestion pipeline
├── ingest_news.py                  # Google News RSS headline scraper
├── requirements.txt                # Project dependencies
└── stocklens.db                    # SQLite database (Prices & FTS5 News index)

``
---

## 🔄 System Flow

yfinance (Market Prices) ──► ingest.py ─────────┐
├──► SQLite Database (stocklens.db)
Google News RSS ─────────► ingest_news.py ──────┘            │
▼
Streamlit Multi-Page Dashboard
│
┌────────────────────────────────────────┼────────────────────────────────────────┐
▼                                        ▼                                        ▼
Dashboard & Technicals               Investment Lens & Signals              AI Research Assistant (Ask)
(20/50 SMA, Volatility, Returns)        (Dynamic RSI, Tax & ROI Calculator)       (Grounded Gemini Answers + Citations)


---

## ⚙️ Setup & Installation

### 1. Prerequisites
- Python 3.10+
- pip

### 2. Clone Repository
```bash
git clone [https://github.com/PRANAV-MS25/stocklens.git](https://github.com/PRANAV-MS25/stocklens.git)
cd stocklens
3. Create & Activate Virtual Environment
Bash
python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On Linux/macOS:
# source .venv/bin/activate
4. Install Dependencies
Bash
pip install -r requirements.txt
5. Configure API Key
Create a .env file in the project root directory and add your free Google Gemini API key:

Code snippet
GEMINI_API_KEY=your-gemini-api-key-here
6. Run Ingestion Pipeline
Fetch historical price bars and real-time news headlines into SQLite:

Bash
python ingest.py
python ingest_news.py
7. Launch Application
Bash
python -m streamlit run app.py
Open: http://localhost:8501

🧪 Running Unit Tests
To verify quantitative signal logic and tax calculation models:

Bash
python -m pytest tests/
🛠️ Tech Stack
Core & Analytics: Python, Pandas, NumPy, SQLite (FTS5)

Frontend & Visualizations: Streamlit, Plotly Express, Plotly Graph Objects

Data Ingestion: yfinance, Google News RSS

AI & NLP: Google Gemini API (google-genai)
