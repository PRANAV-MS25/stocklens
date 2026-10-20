# StockLens

A research assistant for 20 large Indian stocks (NSE). It collects daily prices and news headlines, shows trends and comparisons on a dashboard, and answers questions using only the stored data, citing the headlines it used.

> Research tool only. Nothing here is investment advice.

![Ask page](docs/ask.png)

## What it does

- **Dashboard:** price with 20 and 50-day moving averages, returns, annualized volatility and volume for any of 20 stocks.
- **Compare:** rebases several stocks to 100, shows best and worst performer, and a correlation table of daily returns.
- **News:** collects recent headlines per company into a searchable full-text index and shows them next to price charts.
- **Ask:** takes a question in plain language, finds the matching stock and headlines, adds computed price facts, and asks an LLM to answer using only that context, with numbered sources.

## How it works

```
yfinance (prices) ──► ingest.py ───────┐
                                       ├──► SQLite (stocklens.db)
Google News RSS ───► ingest_news.py ───┘          │
                                                  ▼
                              Streamlit app: dashboard, compare, news
                                                  │
                          question ──► ticker match + headline search
                                                  │
                         price facts + headlines ──► Gemini ──► cited answer
```

Design choices:

- **Numbers come from code, not the model.** Returns, volatility and moves are computed with pandas and passed to the model as facts.
- **Grounded answers.** The prompt tells the model to answer only from the provided context, to say so when the data does not explain a price move, and never to give buy/sell advice or predictions.
- **Headlines are treated as untrusted input.** They are passed as data, and the prompt forbids following instructions found inside them.
- **Headlines only.** Only titles, sources, dates and links are stored, and every item links back to the publisher.

## Run it locally

```
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python ingest.py
python ingest_news.py
```

Create a `.env` file in the project folder with a free Gemini API key from Google AI Studio:

```
GEMINI_API_KEY=your-key
```

Then start the app:

```
python -m streamlit run app.py
```

## Limitations

- Only 20 stocks, and about two years of daily data.
- Prices come from yfinance, which is free and can be delayed or occasionally wrong.
- The assistant sees headlines, not full articles, so it often cannot say why a stock moved. In that case it says so.
- Data refresh is manual for now (`ingest.py` and `ingest_news.py`).

## Roadmap

- Automated tests for the return, volatility and ticker-matching logic
- Scheduled data refresh and a live deployment
- Backtest of simple signals against buy-and-hold
- Optional daily briefing notifications

## Tech

Python, pandas, SQLite (with FTS5 full-text search), Streamlit, yfinance, Google Gemini API.