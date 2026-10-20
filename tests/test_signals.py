import pytest
import pandas as pd
import numpy as np

def calculate_rsi(prices: pd.Series, period: int = 14) -> pd.Series:
    """Helper function to test RSI calculation logic."""
    delta = prices.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def calculate_stcg_tax(gross_profit: float, tax_rate: float = 0.20) -> float:
    """Helper function to test tax calculation logic."""
    if gross_profit <= 0:
        return 0.0
    return gross_profit * tax_rate


# --- UNIT TESTS ---

def test_rsi_bounds():
    """Verify that RSI values always stay within 0 and 100."""
    price_data = pd.Series([100, 102, 101, 105, 107, 106, 110, 108, 112, 115, 114, 118, 120, 119, 122, 125])
    rsi_series = calculate_rsi(price_data)
    valid_rsi = rsi_series.dropna()
    
    assert (valid_rsi >= 0).all(), "RSI contains negative values"
    assert (valid_rsi <= 100).all(), "RSI exceeds 100"

def test_rsi_oversold_signal():
    """Verify that a consecutive downward trend drops RSI into oversold territory (< 35)."""
    decreasing_prices = pd.Series([100 - i * 2 for i in range(20)])
    rsi_series = calculate_rsi(decreasing_prices)
    latest_rsi = rsi_series.iloc[-1]
    
    assert latest_rsi < 35, f"Expected oversold RSI (<35), but got {latest_rsi}"

def test_tax_calculator_positive_profit():
    """Verify 20% STCG calculation on profit."""
    profit = 10000.0
    expected_tax = 2000.0
    calculated_tax = calculate_stcg_tax(profit, tax_rate=0.20)
    
    assert calculated_tax == expected_tax, f"Expected tax {expected_tax}, got {calculated_tax}"

def test_tax_calculator_loss():
    """Verify that capital gain tax is 0 on losses."""
    loss = -5000.0
    calculated_tax = calculate_stcg_tax(loss, tax_rate=0.20)
    
    assert calculated_tax == 0.0, f"Expected 0 tax on loss, got {calculated_tax}"