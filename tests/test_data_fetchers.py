from types import SimpleNamespace

import pandas as pd
import pytest

from financial_data import data_fetchers


def _simfin_frame(ticker, rows):
    # rows: {report_date: {column: value}}; mimics SimFin's (Ticker, Report Date) index
    index = pd.MultiIndex.from_tuples(
        [(ticker, pd.Timestamp(d)) for d in rows], names=["Ticker", "Report Date"]
    )
    return pd.DataFrame(list(rows.values()), index=index)


def _yf_frame(rows):
    # rows: {report_date: {yfinance row label: value}}; yfinance has labels as rows, dates as columns
    return pd.DataFrame({pd.Timestamp(d): values for d, values in rows.items()})


@pytest.fixture
def sources(monkeypatch):
    data_fetchers._load_simfin_statements.cache_clear()
    monkeypatch.setenv("SIMFIN_API_KEY", "test-key")
    monkeypatch.setattr(data_fetchers.sf, "set_data_dir", lambda path: None)
    monkeypatch.setattr(data_fetchers.sf.config, "set_api_key", lambda api_key: None)

    simfin_data = {
        "load_income": _simfin_frame("AAPL", {"2023-03-31": {"Revenue": 100, "Net Income": 10}}),
        "load_balance": _simfin_frame("AAPL", {"2023-03-31": {"Total Assets": 500}}),
        "load_cashflow": _simfin_frame("AAPL", {"2023-03-31": {"Net Cash from Operating Activities": 50}}),
    }
    for name, frame in simfin_data.items():
        monkeypatch.setattr(data_fetchers.sf, name, lambda variant, market, frame=frame: frame)

    yf_data = {
        "2023-03-31": {"Total Revenue": 999, "Net Income": 99},  # Overlaps SimFin; SimFin should win
        "2023-06-30": {"Total Revenue": 200, "Net Income": 20},  # Newer quarter only in yfinance
    }
    fake_ticker = SimpleNamespace(
        quarterly_income_stmt=_yf_frame(yf_data),
        quarterly_balance_sheet=_yf_frame({"2023-06-30": {"Total Assets": 600}}),
        quarterly_cashflow=pd.DataFrame(),
    )
    monkeypatch.setattr(data_fetchers.yf, "Ticker", lambda ticker: fake_ticker)
    return simfin_data


def test_get_simfin_api_key_raises_when_missing(monkeypatch):
    monkeypatch.delenv("SIMFIN_API_KEY", raising=False)
    with pytest.raises(ValueError, match="SIMFIN_API_KEY"):
        data_fetchers.get_simfin_api_key()


def test_get_fred_api_returns_env_value(monkeypatch):
    monkeypatch.setenv("FRED_API_KEY", "fred-123")
    assert data_fetchers.get_fred_api() == "fred-123"


def test_income_merges_simfin_and_yfinance(sources):
    income, _, _ = data_fetchers.get_fundamental_data("AAPL")

    assert list(income.columns) == list(data_fetchers.INCOME_STATEMENT_MAP.values())
    assert income.index.is_monotonic_increasing
    assert income.loc[pd.Timestamp("2023-03-31"), "Revenue"] == 100  # SimFin value kept
    assert income.loc[pd.Timestamp("2023-06-30"), "Revenue"] == 200  # yfinance-only quarter added


def test_missing_yfinance_rows_become_nan(sources):
    income, _, _ = data_fetchers.get_fundamental_data("AAPL")

    # yfinance did not report Pretax Income, so the column is NaN rather than raising KeyError
    assert income["Pretax Income (Loss)"].isna().all()


def test_empty_yfinance_statement_still_returns_simfin_columns(sources):
    _, _, cash_flow = data_fetchers.get_fundamental_data("AAPL")

    assert list(cash_flow.columns) == list(data_fetchers.CASH_FLOW_MAP.values())
    assert cash_flow.iloc[0]["Net Cash from Operating Activities"] == 50


def test_ticker_missing_from_simfin_uses_yfinance_only(sources, monkeypatch):
    # SimFin only covers MSFT here, so AAPL should come entirely from yfinance
    monkeypatch.setattr(
        data_fetchers.sf,
        "load_income",
        lambda variant, market: _simfin_frame("MSFT", {"2023-03-31": {"Revenue": 1}}),
    )
    income, _, _ = data_fetchers.get_fundamental_data("AAPL")

    assert income.loc[pd.Timestamp("2023-03-31"), "Revenue"] == 999
    assert len(income) == 2


def test_simfin_is_downloaded_once_per_session(sources, monkeypatch):
    calls = []
    monkeypatch.setattr(
        data_fetchers.sf,
        "load_income",
        lambda variant, market: calls.append(1) or sources["load_income"],
    )
    data_fetchers.get_fundamental_data("AAPL")
    data_fetchers.get_fundamental_data("AAPL")

    assert len(calls) == 1
