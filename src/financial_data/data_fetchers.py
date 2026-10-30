# Fetch company fundamentals from SimFin (long history) and yfinance (recent quarters)
import os
from functools import lru_cache

import pandas as pd
import simfin as sf
import yfinance as yf
from dotenv import load_dotenv

# Load API keys from the project's .env file (gitignored)
load_dotenv()

# Each mapping stores the yfinance row name as key and the SimFin column name as value
INCOME_STATEMENT_MAP = {
    "Total Revenue": "Revenue",
    "Operating Income": "Operating Income (Loss)",
    "Pretax Income": "Pretax Income (Loss)",
    "Net Income": "Net Income",
}

BALANCE_SHEET_MAP = {
    "Total Assets": "Total Assets",
    "Total Liabilities Net Minority Interest": "Total Liabilities",
    "Current Assets": "Total Current Assets",
    "Current Liabilities": "Total Current Liabilities",
    "Stockholders Equity": "Total Equity",
    "Retained Earnings": "Retained Earnings",
    "Long Term Debt": "Long Term Debt",
}

CASH_FLOW_MAP = {
    "Operating Cash Flow": "Net Cash from Operating Activities",
    "Investing Cash Flow": "Net Cash from Investing Activities",
    "Financing Cash Flow": "Net Cash from Financing Activities",
}


def _get_api_key(env_name):
    # Read the key from the environment and fail early if it is missing
    api_key = os.getenv(env_name)
    if not api_key:
        raise ValueError(f"{env_name} is not set. Add it to your .env file.")
    return api_key


def get_simfin_api_key():
    return _get_api_key("SIMFIN_API_KEY")


def get_fred_api():
    return _get_api_key("FRED_API_KEY")


def get_cryptocompare_api():
    return _get_api_key("CRYPTOCOMPARE_API_KEY")


@lru_cache(maxsize=None)
def _load_simfin_statements(statement):
    # Download the full SimFin US quarterly dataset once per session, not once per ticker
    sf.set_data_dir(os.path.expanduser("~/simfin_data/"))
    sf.config.set_api_key(api_key=get_simfin_api_key())

    loaders = {
        "income": sf.load_income,
        "balance": sf.load_balance,
        "cashflow": sf.load_cashflow,
    }
    return loaders[statement](variant="quarterly", market="us")


def _build_statement(simfin_statement, yf_attribute, asset_ticker, asset_yf, mapping):
    # Get the SimFin rows for the ticker; tickers SimFin does not cover return an empty frame
    simfin_all = _load_simfin_statements(simfin_statement)
    if asset_ticker in simfin_all.index.get_level_values(0):
        simfin_df = simfin_all.loc[asset_ticker, :]
    else:
        simfin_df = pd.DataFrame()

    # Get the yfinance statement with dates as rows, using the SimFin column names
    yf_df = getattr(asset_yf, yf_attribute).T.rename(columns=mapping)

    # Keep only the final column list; missing columns become NaN instead of raising KeyError
    columns = list(mapping.values())
    combined = pd.concat([simfin_df.reindex(columns=columns), yf_df.reindex(columns=columns)])

    # Where both sources report the same quarter, keep the SimFin value (listed first)
    combined = combined[~combined.index.duplicated(keep="first")]
    return combined.sort_index()


# Define the utility to get the fundamental data for any asset ticker
def get_fundamental_data(asset_ticker):
    asset_yf = yf.Ticker(asset_ticker)

    income_data = _build_statement(
        "income", "quarterly_income_stmt", asset_ticker, asset_yf, INCOME_STATEMENT_MAP
    )
    balance_sheet_data = _build_statement(
        "balance", "quarterly_balance_sheet", asset_ticker, asset_yf, BALANCE_SHEET_MAP
    )
    cash_flow_data = _build_statement(
        "cashflow", "quarterly_cashflow", asset_ticker, asset_yf, CASH_FLOW_MAP
    )

    # Return the income statement, balance sheet and cashflow data
    return income_data, balance_sheet_data, cash_flow_data
