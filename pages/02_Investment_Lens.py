import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="StockLens - Investment & Profit Workbench", layout="wide")

st.title("🎯 Dynamic Investment Lens & Real-Time Profit Calculator")
st.markdown("Select an NSE stock and time duration to dynamically analyze real-time buy signals, ROI, and long-term projections.")

# List of all 20 tracked NSE Stocks
NSE_STOCKS = [
    "RELIANCE.NS", "TCS.NS", "INFY.NS", "HDFCBANK.NS", "ICICIBANK.NS",
    "BHARTIARTL.NS", "ITC.NS", "SBIN.NS", "LTIM.NS", "LT.NS",
    "HINDUNILVR.NS", "AXISBANK.NS", "KOTAKBANK.NS", "TATAMOTORS.NS", "MARUTI.NS",
    "SUNPHARMA.NS", "NTPC.NS", "ULTRACEMCO.NS", "TITAN.NS", "BAJFINANCE.NS"
]

# Sidebar Controls (Default duration set to 1y)
ticker_input = st.sidebar.selectbox("Select NSE Stock", options=NSE_STOCKS, index=0)
period = st.sidebar.selectbox("Historical Data Range (Duration)", ["3mo", "6mo", "1y", "2y", "5y"], index=2)

@st.cache_data(ttl=300)
def fetch_stock_details(symbol, timeframe):
    ticker = yf.Ticker(symbol)
    df = ticker.history(period=timeframe)
    info = ticker.info
    return df, info

try:
    df, info = fetch_stock_details(ticker_input, period)
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
    
    pe_val = info.get('trailingPE', None)
    col4.metric("Trailing P/E Ratio", f"{pe_val:.2f}" if pe_val else "N/A")

    st.markdown("---")

    # SECTION 1: TIME-FRAME DYNAMIC SIGNAL & OUTLOOK
    st.subheader(f"📊 Signal & Outlook for Selected Horizon ({period})")

    # Dynamic Moving Averages (adjusted window size if data points are fewer than period)
    ma_short_window = min(20, max(len(df) // 4, 3))
    ma_long_window = min(50, max(len(df) // 2, 5))

    df['SMA_Short'] = df['Close'].rolling(ma_short_window).mean()
    df['SMA_Long'] = df['Close'].rolling(ma_long_window).mean()

    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))

    latest_rsi = df['RSI'].iloc[-1] if not pd.isna(df['RSI'].iloc[-1]) else 50.0
    sma_short = df['SMA_Short'].iloc[-1]
    sma_long = df['SMA_Long'].iloc[-1]
    period_return = ((df['Close'].iloc[-1] - df['Close'].iloc[0]) / df['Close'].iloc[0]) * 100

    # Dynamic Signal Logic based on Selected Duration Performance
    signal_score = 0
    reasons = []

    if current_price > sma_short and sma_short > sma_long:
        signal_score += 2
        reasons.append(f"Bullish Trend over {period}: Price is trading above short and long moving averages.")
    elif current_price < sma_short:
        signal_score -= 1
        reasons.append(f"Short-term pullback: Price is below the moving average for the {period} window.")

    if latest_rsi < 35:
        signal_score += 2
        reasons.append(f"Oversold Momentum: RSI stands at {latest_rsi:.1f} (Attractive entry point).")
    elif latest_rsi > 70:
        signal_score -= 2
        reasons.append(f"Overbought Momentum: RSI stands at {latest_rsi:.1f} (Risk of near-term correction).")
    else:
        reasons.append(f"Balanced Momentum: RSI is neutral at {latest_rsi:.1f}.")

    if period_return > 15:
        signal_score += 1
        reasons.append(f"Strong historical growth of +{period_return:.1f}% over the chosen {period} horizon.")
    elif period_return < -5:
        signal_score += 1  # Dip buying opportunity
        reasons.append(f"The stock is down {period_return:.1f}% over {period}, presenting a potential discount/dip buy.")

    # Render dynamic color-coded recommendation boxes
    if signal_score >= 3:
        st.success(f"🟢 **STRONG ACCUMULATE / BUY ({period.upper()} HORIZON)**")
    elif signal_score >= 1:
        st.info(f"🟡 **HOLD / MODERATE ACCUMULATION ({period.upper()} HORIZON)**")
    else:
        st.warning(f"🔴 **CAUTION / AWAIT DIP ({period.upper()} HORIZON)**")

    with st.expander(f"🔍 Dynamic Signal Breakdown ({period})"):
        for r in reasons:
            st.write(f"• {r}")

    st.markdown("---")

    # SECTION 2: REAL-TIME PROFIT & TAX CALCULATOR
    st.subheader("💰 Investment Profit & Tax Calculator")
    calc_col1, calc_col2 = st.columns(2)

    with calc_col1:
        shares = st.number_input("Number of Shares Bought", min_value=1, value=50)
        default_buy_price = float(round(current_price * 0.95, 2))
        buy_price = st.number_input("Purchase Price per Share (₹)", min_value=1.0, value=default_buy_price)
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

    # SECTION 3: LONG-RUN COMPOUNDING PROJECTION
    st.subheader("🚀 Long-Run Wealth Projection (1 to 5 Years)")
    
    annualized_return = max(float(period_return / 100), 0.08)

    years = np.arange(1, 6)
    projected_values = [current_val * ((1 + annualized_return) ** yr) for yr in years]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=[f"Year {y}" for y in years],
        y=projected_values,
        text=[f"₹{v:,.0f}" for v in projected_values],
        textposition='auto',
        marker_color='#00CC96' if annualized_return > 0 else '#EF553B'
    ))
    fig.update_layout(
        title=f"Projected Wealth Growth based on selected {period} performance ({annualized_return*100:.1f}% Annualized)",
        xaxis_title="Timeline",
        yaxis_title="Portfolio Value (₹)",
        template="plotly_dark"
    )
    st.plotly_chart(fig, use_container_width=True)

except Exception as e:
    st.error(f"Error executing analysis: {e}")