# 📈 StockLens — Quantitative Market Assistant & AI Research Engine

StockLens is a full-stack financial analytics, technical research, and grounded AI assistant web app for Indian Stock Exchange (NSE) equities. It automates daily price action ingestion, computes dynamic trading signals, calculates real-time tax liabilities and wealth compounding projections, and provides cited AI answers powered by Google Gemini.

> ⚠️ **Disclaimer:** Research tool only. Nothing here constitutes professional financial or investment advice.

---

## 📁 Project Structure

stocklens/├── pages/                          # Streamlit multi-page views│   ├── 02_Investment_Lens.py       # Dynamic buy/hold signals, tax & ROI calculator│   ├── 3_News.py                   # Google News RSS aggregator & FTS search│   ├── 4_Ask.py                    # Grounded AI research assistant (Gemini API)│   └── 5_Peer_Benchmark.py         # Multi-stock risk/return scatter & correlation heatmap├── tests/                          # Automated testing suite│   ├── test_core.py                # Core mathematical indicator tests│   └── test_signals.py             # RSI momentum & tax calculator tests├── docs/                           # Documentation assets & screenshots│   └── ask.png                     # UI preview screenshot├── .env                            # Environment configuration (API Keys)├── .gitignore                      # Git ignore rules├── app.py                          # Main Streamlit dashboard entrypoint├── core.py                         # Analytics core (returns, volatility, metrics)├── conftest.py                     # Pytest root configuration├── ingest.py                       # Historical & daily price bar fetcher├── ingest_news.py                  # Google News RSS scraper into SQLite FTS5├── notify_test.py                  # Alert testing script├── requirements.txt                # Python dependencies└── stocklens.db                    # SQLite database (Prices + FTS5 News index)
---

## 🗄️ Database Schema

### `prices`
| Field | Type | Description |
|-------|------|-------------|
| ticker | VARCHAR | NSE Stock Symbol (e.g., `RELIANCE.NS`) |
| date | DATETIME | Trading session timestamp |
| open | DECIMAL | Opening price |
| high | DECIMAL | Daily high price |
| low | DECIMAL | Daily low price |
| close | DECIMAL | Closing price |
| volume | BIGINT | Total shares traded |

### `news` (SQLite FTS5 Full-Text Search Table)
| Field | Type | Description |
|-------|------|-------------|
| ticker | VARCHAR | Associated NSE symbol |
| headline | TEXT | Scraped news article title |
| date | DATETIME | Publication timestamp |
| url | TEXT | Direct link to original publisher source |

---

## ⚙️ Setup Instructions

### 1. Prerequisites
```bash
Python 3.10+
pip
2. Clone / Extract ProjectBashgit clone [https://github.com/PRANAV-MS25/stocklens.git](https://github.com/PRANAV-MS25/stocklens.git)
cd stocklens
3. Create Virtual EnvironmentBashpython -m venv .venv
source .venv/bin/activate         # Linux/Mac
.venv\Scripts\activate            # Windows
4. Install DependenciesBashpip install -r requirements.txt
5. Configure API KeysCreate a .env file in the project root directory:Code snippetGEMINI_API_KEY=your-gemini-api-key-here
6. Seed / Ingest Initial DataBashpython ingest.py
python ingest_news.py
7. Run the ApplicationBashpython -m streamlit run app.py
Open: http://localhost:8501🔐 Default Environment & API ReferencesComponentProvider / ConfigPurposeDatabaseSQLite (stocklens.db)Local persistent storage for prices & newsMarket Feedyfinance APIReal-time & 2-year daily historical price barsNews FeedGoogle News RSSCompany headline scraperAI EngineGoogle Gemini APIGrounded natural language Q&A engine🔄 System Flowyfinance (Market Prices) ──► ingest.py ─────────┐
                                                 ├──► SQLite Database (stocklens.db)
Google News RSS ─────────► ingest_news.py ──────┘            │
                                                              ▼
                                               Streamlit Multi-Page Dashboard
                                                              │
                     ┌────────────────────────────────────────┼────────────────────────────────────────┐
                     ▼                                        ▼                                        ▼
          Dashboard & Technicals               Investment Lens & Signals              AI Research Assistant (Ask)
     (20/50 SMA, Volatility, Returns)        (Dynamic RSI, Tax & ROI Calculator)       (Grounded Gemini Answers + Citations)
🌐 URL / Page ReferencePage FileRouteDescriptionapp.py/Main market dashboard, price moving averages, and volumepages/02_Investment_Lens.py/Investment_LensTimeframe-bound signals, STCG tax, & 5-year ROI projectionspages/5_Peer_Benchmark.py/Peer_BenchmarkMulti-stock base-100 chart, Sharpe ratio matrix, & heatmapspages/3_News.py/NewsSearchable SQLite full-text RSS news aggregatorpages/4_Ask.py/AskGrounded AI research copilot with inline citations✅ Features ImplementedAutomated price & news ingestion pipelines storing into SQLite (FTS5)Interactive market dashboard with 20 & 50-day moving average overlaysDynamic timeframe-bound investment signal evaluator (3mo, 1y, 2y, 5y)Real-time trade ROI calculator with Short-Term Capital Gains (STCG) tax deductions5-year annualized wealth compounding projection bar chartPeer benchmark workspace with base-100 price normalizationQuantitative Sharpe Ratio risk-adjusted performance table & scatter matrixCross-stock return correlation matrix heatmap using PlotlyGrounded Gemini AI copilot synthesizing pandas calculations with cited headlinesUnit testing suite (pytest) covering signal generation & tax logic📸 Project Screenshots1. Dashboard & Core TechnicalsMain DashboardPeer Benchmark Matrix2. Investment Workbench & AI AssistantInvestment Lens & Signal CalculatorGrounded AI Assistant
