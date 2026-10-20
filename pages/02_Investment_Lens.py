import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="StockLens - Investment & Profit Workbench", layout="wide")

st.title("🎯 Investment Signals & Real-Time Profit Calculator")
st.markdown("Automated signal evaluation, live trade ROI calculator, and long-term holding projections.")

# Sidebar inputs
ticker_input = st.sidebar.text_input("Enter NSE Stock Ticker (e.g., RELIANCE.NS, TCS.NS, INFYS.NS)", value="RELIANCE.NS")
period = st.sidebar.selectbox("Historical Data Range", ["6mo", "1y", "2y", "5y"], index=1)

@st.cache_data(ttl=300)
def fetch_stock_details(symbol):
    ticker = yf.Ticker(symbol)
    df = ticker.history(period=period)
    info = ticker.info
    return df, info

try:
    df, info = fetch_stock_details(ticker_input)
    if df.empty:
        st.error("Could not retrieve stock data. Please verify the ticker symbol.")
        st.stop()

    current_price = df['Close'].iloc[-1]
    prev_close = df['Close'].iloc[-2]
    day_change = ((current_price - prev_close) / prev_close) * 100

    # Key Metrics Bar
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Current Live Price", f"₹{current_price:,.2f}", f"{day_change:+.2f}%")
    col2.metric("52-Week High", f"₹{info.get('fiftyTwoWeekHigh', 0):,.2f}")
    col3.metric("52-Week Low", f"₹{info.get('fiftyTwoWeekLow', 0):,.2f}")
    col4.metric("Trailing P/E Ratio", f"{info.get('trailingPE', 'N/A')}")

    st.markdown("---")

    # SECTION 1: AUTO BUY / SELL / HOLD SIGNAL
    st.subheader("📊 Stock Lens Signal & Long-Run Outlook")

    # Calculate Moving Averages & RSI
    df['SMA_20'] = df['Close'].rolling(20).mean()
    df['SMA_50'] = df['Close'].rolling(50).mean()

    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))

    latest_rsi = df['RSI'].iloc[-1]
    sma_20 = df['SMA_20'].iloc[-1]
    sma_50 = df['SMA_50'].iloc[-1]

    # Signal Logic
    signal_score = 0
    reasons = []

    if current_price > sma_20 and sma_20 > sma_50:
        signal_score += 2
        reasons.append("Bullish Trend: Price is above both 20-day and 50-day Moving Averages.")
    elif current_price < sma_20:
        signal_score -= 1
        reasons.append("Short-term Pullback: Price is trading below 20-day Moving Average.")

    if latest_rsi < 35:
        signal_score += 2
        reasons.append(f"Oversold Condition: RSI is at {latest_rsi:.1f} (Potential Entry Point).")
    elif latest_rsi > 70:
        signal_score -= 2
        reasons.append(f"Overbought Condition: RSI is at {latest_rsi:.1f} (Risk of Correction).")
    else:
        reasons.append(f"Neutral Momentum: RSI is balanced at {latest_rsi:.1f}.")

    pe = info.get('trailingPE', None)
    if pe and pe < 25:
        signal_score += 1
        reasons.append(f"Reasonable Valuation: Trailing P/E is {pe:.1f}.")

    # Output Recommendation
    if signal_score >= 3:
        st.success("🟢 **STRONG ACCUMULATE / BUY**")
    elif signal_score >= 1:
        st.info("🟡 **HOLD / MODERATE ACCUMULATION**")
    else:
        st.warning("🔴 **CAUTION / AWAIT DIP**")

    with st.expander("🔍 Signal Reasoning Breakdown"):
        for r in reasons:
            st.write(f"• {r}")

    st.markdown("---")

    # SECTION 2: REAL-TIME PROFIT & TAX CALCULATOR
    st.subheader("💰 Investment Profit & Tax Calculator")
    calc_col1, calc_col2 = st.columns(2)

    with calc_col1:
        shares = st.number_input("Number of Shares Bought", min_value=1, value=50)
        buy_price = st.number_input("Purchase Price per Share (₹)", min_value=1.0, value=float(round(current_price * 0.95, 2)))
        stcg_rate = st.slider("Short Term Capital Gain Tax Rate (%)", min_value=0, max_value=30, value=20)

    with calc_col2:
        invested_val = shares * buy_price
        current_val = shares * current_price
        gross_profit = current_val - invested_val
        roi = (gross_profit / invested_val) * 100 if invested_val > 0 else 0

        tax_amount = (gross_profit * (stcg_rate / 100)) if gross_profit > 0 else 0
        net_profit = gross_profit - tax_amount

        st.markdown(f"**Total Invested:** ₹{invested_val:,.2f}")
        st.markdown(f"**Current Value:** ₹{current_val:,.2f}")
        st.markdown(f"**Gross Profit / Loss:** ₹{gross_profit:,.2f} (`{roi:+.2f}%`)")
        st.markdown(f"**Est. Tax Liability:** ₹{tax_amount:,.2f}")
        st.metric("Net Profit (After Tax)", f"₹{net_profit:,.2f}")

    st.markdown("---")

    # SECTION 3: LONG-RUN COMPOUNDING PROJECTION (5-YEAR HORIZON)
    st.subheader("🚀 Long-Run Wealth Projection (1 to 5 Years)")
    
    # Calculate historical 1-year return for baseline
    one_year_return = ((df['Close'].iloc[-1] - df['Close'].iloc[0]) / df['Close'].iloc[0])
    annualized_return = max(float(one_year_return), 0.08)  # Default fallback 8%

    years = np.arange(1, 6)
    projected_values = [current_val * ((1 + annualized_return) ** yr) for yr in years]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=[f"Year {y}" for y in years],
        y=projected_values,
        text=[f"₹{v:,.0f}" for v in projected_values],
        textposition='auto',
        marker_color='#00CC96'
    ))
    fig.update_layout(
        title=f"Projected Long-Term Growth at {annualized_return*100:.1f}% Annualized Return",
        xaxis_title="Timeline",
        yaxis_title="Portfolio Value (₹)",
        template="plotly_dark"
    )
    st.plotly_chart(fig, use_container_width=True)

except Exception as e:
    st.error(f"Error executing analysis: {e}")