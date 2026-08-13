# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an educational repository following the "Getting Market Data: Stocks, Crypto, News & Fundamentals" course. The project builds practical skills in retrieving, validating, cleaning, and preparing financial market data for quantitative analysis and investment research.

**Key Focus Areas:**
- Pricing & Market Data (equities, FX, crypto, derivatives)
- Company Data (fundamentals, financial statements, valuations, corporate actions)
- Economic Data (GDP, inflation, interest rates)
- Unstructured Data (financial news, sentiment analysis)
- Data Quality Checks & Cleaning
- Building reusable financial data pipelines

## Environment Setup

### Python & Dependencies

This project requires **Python 3.11+** and uses a virtual environment with key financial data libraries.

**Initial Setup:**
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

**Key Libraries:**
- `pandas` / `numpy` - Data manipulation and numerical computing
- `yfinance` - Yahoo Finance data (stocks, crypto, indices)
- `requests` - HTTP requests for APIs
- `jupyter` / `jupyterlab` - Interactive notebooks for exploration
- `python-dotenv` - Environment variable management (for API keys)
- `pytest` - Testing framework

### API Key Management

Financial data retrieval often requires API keys. **Never commit API keys or credentials.**

**Best Practice:**
- Store API keys in a `.env` file (included in `.gitignore`)
- Load keys at runtime using `python-dotenv`:
  ```python
  from dotenv import load_dotenv
  import os
  
  load_dotenv()
  api_key = os.getenv('FINANCIAL_API_KEY')
  ```
- Document required environment variables in `.env.example` without actual values

## Common Development Tasks

### Running Jupyter Notebooks
```bash
jupyter lab  # Or: jupyter notebook
```
The repository will primarily use Jupyter notebooks for exploration and learning. Notebooks live in `notebooks/` organized by topic (pricing, company_data, economic_data, etc.).

### Running Tests
```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_data_cleaning.py

# Run with verbose output
pytest -v
```

### Code Quality
```bash
# Format code
black .

# Lint
flake8 .

# Type checking (if applicable)
mypy .
```

### Working with Financial Data

When building data pipelines:
1. **Source the data** - Use APIs (yfinance, requests, etc.)
2. **Validate** - Check for missing values, duplicates, timestamp issues
3. **Clean** - Handle gaps, normalize formats, align frequencies
4. **Transform** - Prepare for analysis (resampling, rolling windows, etc.)
5. **Verify** - Ensure data quality before downstream use

## Repository Architecture

```
financial-market-data-python/
├── notebooks/              # Jupyter notebooks organized by topic
│   ├── 01_pricing_data/   # Stocks, indices, crypto, derivatives
│   ├── 02_company_data/   # Fundamentals, financial statements, etc.
│   ├── 03_economic_data/  # Macro indicators
│   ├── 04_unstructured/   # News, sentiment data
│   └── 05_data_quality/   # Validation and cleaning examples
├── src/                   # Reusable Python modules (as project scales)
│   └── financial_data/
│       ├── data_fetchers.py      # API integrations
│       ├── validators.py          # Data quality checks
│       ├── cleaners.py            # Data transformation
│       └── pipelines.py           # End-to-end workflows
├── tests/                 # Unit tests for reusable code
├── data/                  # Local data storage (CSV, parquet)
├── .env.example           # Template for API keys
├── requirements.txt       # Python dependencies
└── README.md             # Project overview
```

### Key Design Principles

- **Notebook-Driven Learning**: Most content starts in notebooks for exploration
- **Modular Extraction**: As patterns emerge, extract reusable code into `src/`
- **Pipeline Orientation**: Build end-to-end workflows from data retrieval to preparation
- **Data Validation First**: Implement quality checks before processing
- **API Abstraction**: Create simple wrappers around financial API calls for consistency

## Working with Financial Datasets

### Common Data Issues to Watch For
- **Missing data**: Holidays, trading halts, API gaps
- **Duplicates**: Same OHLCV data from multiple sources
- **Timestamp misalignment**: Different timezones, trading hours, frequencies
- **Corporate actions**: Stock splits, dividends affecting historical prices
- **Data gaps**: Delisted securities, API outages, coverage gaps
- **Outliers**: Data errors vs. legitimate market moves

### Recommended Workflow
1. Start with notebook exploration to understand data structure
2. Write validation checks to identify issues
3. Implement cleaning logic incrementally
4. Extract utilities into `src/` as they stabilize
5. Add tests for critical transformations

## Development Notes

- **API Rate Limits**: Many financial APIs (especially free tiers) have rate limits. Build in delays and caching
- **Data Freshness**: Real-time vs. historical data has different requirements and costs
- **Multiple Sources**: Cross-reference data from multiple providers when possible
- **Documentation**: Financial data is heavily domain-specific; document data sources and transformations
- **Reproducibility**: Use fixed seeds and version pinning for research notebooks

## Git Workflow

```bash
# For course exercises and explorations
git add notebooks/
git commit -m "Add [topic] exploration notebook"

# For reusable code
git add src/
git commit -m "Add [module] utility for [functionality]"
```

## Useful Financial Data Providers

- **yfinance** - Free stock/crypto/index data (Yahoo Finance)
- **FRED** - Federal Reserve economic data (US macro)
- **Alpha Vantage** - Stock, forex, crypto (API key required)
- **Finnhub** - News, fundamentals, real-time data
- **IEX Cloud** - Comprehensive financial data
- **Polygon.io** - Market data and alternatives
- **NewsAPI** - Financial news aggregation

## Future Enhancements

As the repository grows, consider:
- Automated data pipeline orchestration (Airflow, Prefect)
- Database integration (PostgreSQL, ClickHouse) for large datasets
- Caching strategies for API calls
- Visualization dashboards (Plotly, Streamlit)
- Backtesting frameworks for strategy validation
- ML/NLP pipeline for news sentiment analysis
