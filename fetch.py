import yfinance as yf

df = yf.Ticker("TCS.NS").history(period="1y")
print(df[["Close", "Volume"]].tail())
print(f"1-year return: {df['Close'].iloc[-1] / df['Close'].iloc[0] - 1:.1%}")