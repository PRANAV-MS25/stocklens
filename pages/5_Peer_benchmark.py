import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="StockLens - Peer Benchmark", layout="wide")

st.title("⚖️ Peer Comparison & Risk-Return Analysis")
st.markdown("Compare multiple NSE stocks head-to-head on normalized returns, volatility, risk-adjusted performance, and correlation.")

# Sidebar Controls
default_tickers = ["RELIANCE.NS", "TCS.NS", "INFY.NS", "HDFCBANK.NS"]
selected_tickers = st.sidebar.multiselect(
    "Select Stocks to Compare (NSE)",
    options=["RELIANCE.NS", "TCS.NS", "INFY.NS", "HDFCBANK.NS", "ICICIBANK.NS", "BHARTIARTL.NS", "ITC.NS", "LT.NS", "SBIN.NS", "TATAMOTORS.NS"],
    default=default_tickers
)

time_period = st.sidebar.selectbox("Lookback Window", ["3mo", "6mo", "1y", "2y", "5y"], index=2)

if len(selected_tickers) < 2:
    st.info("💡 Please select at least 2 stocks in the sidebar to perform comparison.")
    st.stop()

@st.cache_data(ttl=300)
def fetch_benchmark_data(tickers, period):
    data = yf.download(tickers, period=period)['Close']
    if isinstance(data, pd.Series):
        data = data.to_frame()
    return data

try:
    prices = fetch_benchmark_data(selected_tickers, time_period)
    prices = prices.dropna()

    if prices.empty:
        st.error("No price data retrieved for the selected stocks.")
        st.stop()

    # SECTION 1: RELATIVE CUMULATIVE RETURN (Normalized to 100)
    st.subheader("📈 Growth Trajectory (Normalized Return Base 100)")
    st.caption("Shows percentage growth comparison assuming ₹100 invested in each stock at start date.")

    normalized_prices = (prices / prices.iloc[0]) * 100

    fig_norm = px.line(
        normalized_prices,
        labels={"value": "Indexed Performance (Base 100)", "Date": "Date"},
        template="plotly_dark"
    )
    fig_norm.update_layout(hovermode="x unified", legend_title="Ticker")
    st.plotly_chart(fig_norm, use_container_width=True)

    st.markdown("---")

    # SECTION 2: METRICS MATRIX (Return vs Volatility vs Sharpe Ratio)
    st.subheader("📊 Quant Performance Matrix")

    daily_returns = prices.pct_change().dropna()
    
    # Metrics calculations
    total_returns = ((prices.iloc[-1] - prices.iloc[0]) / prices.iloc[0]) * 100
    ann_volatility = daily_returns.std() * np.sqrt(252) * 100
    risk_free_rate = 6.5  # Approx India 10Y G-Sec Yield (%)
    ann_return = (1 + (total_returns / 100)) ** (252 / len(prices)) - 1
    sharpe_ratio = ((ann_return * 100) - risk_free_rate) / ann_volatility

    summary_df = pd.DataFrame({
        "Total Return (%)": total_returns.round(2),
        "Annualized Volatility (Risk %)": ann_volatility.round(2),
        "Sharpe Ratio (Risk-Adjusted Return)": sharpe_ratio.round(2)
    })

    col_tbl, col_chart = st.columns([1, 1])

    with col_tbl:
        st.write("#### Performance Summary Table")
        st.dataframe(summary_df, use_container_width=True)
        st.caption("Higher Sharpe Ratio indicates better returns relative to risk taken (Risk-free benchmark ~ 6.5%).")

    with col_chart:
        st.write("#### Risk vs Return Scatter Plot")
        fig_scatter = px.scatter(
            summary_df.reset_index(),
            x="Annualized Volatility (Risk %)",
            y="Total Return (%)",
            color="index",
            size=[15] * len(summary_df),
            text="index",
            template="plotly_dark",
            labels={"index": "Ticker"}
        )
        fig_scatter.update_traces(textposition="top center")
        st.plotly_chart(fig_scatter, use_container_width=True)

    st.markdown("---")

    # SECTION 3: CORRELATION HEATMAP
    st.subheader("🔗 Price Movement Correlation Heatmap")
    st.caption("Values close to +1.0 mean stocks move together; lower values provide better diversification.")

    corr_matrix = daily_returns.corr().round(2)

    fig_corr = px.imshow(
        corr_matrix,
        text_auto=True,
        aspect="auto",
        color_continuous_scale="Blues",
        template="plotly_dark"
    )
    st.plotly_chart(fig_corr, use_container_width=True)

except Exception as e:
    st.error(f"Error computing peer benchmark metrics: {e}")