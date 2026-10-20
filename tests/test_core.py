import pytest

from core import annualized_volatility, find_tickers, period_return


def test_finds_company_by_name():
    assert find_tickers("Why has Infosys moved this week?") == ["INFY.NS"]


def test_is_case_insensitive():
    assert find_tickers("HDFC bank results") == ["HDFCBANK.NS"]


def test_multiple_companies():
    assert set(find_tickers("Compare TCS and Wipro")) == {"TCS.NS", "WIPRO.NS"}


def test_no_company_returns_empty():
    assert find_tickers("Which stock will go up tomorrow?") == []


def test_short_alias_does_not_match_inside_words():
    assert find_tickers("Which switch should I buy?") == []


def test_limit_of_three():
    q = "TCS Infosys Wipro HCL Reliance"
    assert len(find_tickers(q)) == 3


def test_period_return_gain():
    assert period_return([100, 110]) == pytest.approx(0.10)


def test_period_return_loss():
    assert period_return([100, 90, 80]) == pytest.approx(-0.20)


def test_period_return_needs_two_prices():
    with pytest.raises(ValueError):
        period_return([100])


def test_volatility_of_flat_prices_is_zero():
    assert annualized_volatility([100, 100, 100, 100]) == pytest.approx(0.0)


def test_more_swings_means_higher_volatility():
    calm = annualized_volatility([100, 101, 100, 101, 100])
    wild = annualized_volatility([100, 110, 95, 112, 90])
    assert wild > calm