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

python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On Linux/macOS:
# source .venv/bin/activate

```
pip install -r requirements.txt

5. Configure Environment VariablesCreate a .env file in the project root folder and add your free Google Gemini API key:Code snippetGEMINI_API_KEY=your-gemini-api-key-here
6. Run Data Ingestion PipelineFetch historical price bars and real-time news headlines into SQLite:Bashpython ingest.py
python ingest_news.py
7. Launch the Streamlit AppBashpython -m streamlit run app.py
Open: http://localhost:8501🔐 Default Environment & CredentialsComponentConfigurationAccess / SourceDatabaseLocal SQLite (stocklens.db)Auto-generated via ingestion scriptsAI EngineGoogle Gemini API (google-genai)Free tier API key via Google AI StudioMarket DataYahoo Finance (yfinance)Public real-time & historical feeds🔄 System Flowyfinance (Market Prices) ──► ingest.py ─────────┐
                                                 ├──► SQLite Database (stocklens.db)
Google News RSS ─────────► ingest_news.py ───────┘            │
                                                              ▼
                                               Streamlit Multi-Page Dashboard
                                                              │
                     ┌────────────────────────────────────────┼────────────────────────────────────────┐
                     ▼                                        ▼                                        ▼
      Dashboard & Technicals                   Investment Lens & Signals                AI Research Assistant (Ask)
  (20/50 SMA, Volatility, Returns)          (Dynamic RSI, Tax & ROI Calculator)        (Grounded Gemini Answers + Citations)
🌐 URL / Page ReferenceStreamlit PageDescriptionapp.pyMain market dashboard with price trends, moving averages, and volume.pages/02_Investment_Lens.pyDynamic Buy/Hold signal evaluation, capital gains tax calculator, & 5-year compounding projection.pages/5_Peer_Benchmark.pyMulti-stock base-100 normalized performance, Sharpe ratio risk matrix, and correlation heatmaps.pages/3_News.pySearchable FTS5 SQLite news headline aggregator.pages/4_Ask.pyNatural language LLM copilot synthesizing pandas price facts and cited news records.✅ Features ImplementedAutomated Price Ingestion: Fetches historical and daily data for 20 large-cap NSE equities via yfinance.Dynamic Investment Lens: Computes time-frame dependent Buy/Hold/Caution signals (RSI, moving averages, valuation P/E) that update instantly when switching durations (3mo, 1y, 2y, 5y).Real-Time Profit & Tax Calculator: Simulates trade entry returns, calculates gross/net profit, accounts for Short-Term Capital Gains (STCG) tax brackets, and projects 5-year wealth compounding.Peer Benchmark Matrix: Normalizes stock growth to base-100, calculates Sharpe Ratios for risk-adjusted returns, and maps cross-asset return correlations.Grounded AI Copilot: Answers user queries strictly using computed pandas quantitative facts and stored SQLite news context with verified publisher source citations.Automated Unit Testing: Full test coverage (pytest) verifying mathematical accuracy in momentum indicators and tax calculation rules.🧪 Running Unit TestsTo verify quantitative signal logic and tax calculation models:Bashpython -m pytest tests/
📸 Project Screenshots1. Dashboard & Core AnalyticsMain Market DashboardPeer Risk-Return BenchmarkInteractive price tracking & MAsBase-100 normalization & correlation heatmap2. Investment Workbench & AI AssistantInvestment Lens & Signal CalculatorGrounded AI Research AssistantDynamic duration signals & tax breakdownPlain-language Q&A with source citations
