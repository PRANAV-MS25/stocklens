import re

import pandas as pd

ALIASES = {
    "TCS.NS": ["tcs", "tata consultancy"],
    "INFY.NS": ["infosys", "infy"],
    "WIPRO.NS": ["wipro"],
    "HCLTECH.NS": ["hcl", "hcltech"],
    "RELIANCE.NS": ["reliance"],
    "HDFCBANK.NS": ["hdfc"],
    "ICICIBANK.NS": ["icici"],
    "SBIN.NS": ["sbi", "state bank"],
    "ITC.NS": ["itc"],
    "LT.NS": ["l&t", "larsen"],
    "BHARTIARTL.NS": ["airtel", "bharti"],
    "HINDUNILVR.NS": ["hindustan unilever", "hul"],
    "KOTAKBANK.NS": ["kotak"],
    "AXISBANK.NS": ["axis"],
    "MARUTI.NS": ["maruti"],
    "SUNPHARMA.NS": ["sun pharma"],
    "BAJFINANCE.NS": ["bajaj finance"],
    "TITAN.NS": ["titan"],
    "ASIANPAINT.NS": ["asian paints"],
    "ADANIENT.NS": ["adani"],
}


def find_tickers(question, limit=3):
    """Return the tickers whose company names appear in the question."""
    q = question.lower()
    hits = []
    for ticker, names in ALIASES.items():
        if any(re.search(r"\b" + re.escape(n) + r"\b", q) for n in names):
            hits.append(ticker)
    return hits[:limit]


def period_return(closes):
    """Total return over the period, e.g. 0.10 for +10%."""
    closes = list(closes)
    if len(closes) < 2 or closes[0] == 0:
        raise ValueError("need at least two prices and a non-zero first price")
    return closes[-1] / closes[0] - 1


def annualized_volatility(closes, trading_days=252):
    """Standard deviation of daily returns, scaled to a year."""
    daily = pd.Series(list(closes), dtype=float).pct_change().dropna()
    if len(daily) < 2:
        raise ValueError("need at least three prices")
    return float(daily.std() * trading_days ** 0.5)