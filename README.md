# Getting Market Data: Stocks, Crypto, News & Fundamentals

This repository contains my notes, exercises, code examples, and practical implementations from the **Getting Market Data: Stocks, Crypto, News & Fundamentals** course.

The objective of the course is to build a practical understanding of how financial market data can be retrieved, structured, validated, cleaned, and prepared for quantitative analysis, investment research, and financial applications using Python.

Rather than focusing only on price data, the course explores multiple layers of financial information, including market prices, company fundamentals, macroeconomic indicators, corporate events, institutional data, and unstructured information such as financial news.

---

## Course Scope

The repository follows a progressive data pipeline covering several major categories of financial information:

### 1. Pricing & Market Data

Retrieving historical and current market data for different asset classes.

Topics include:

- Equities
  - Stocks
  - Stock indices

- FX & Crypto
  - Foreign exchange markets
  - Cryptocurrencies

- Derivatives
  - Futures
  - Options

The goal is to understand how different instruments are represented by financial data providers and how their time series can be retrieved and standardized.

---

## 2. Company Data

Beyond market prices, the course explores company-specific information that can be used for fundamental and investment analysis.

Topics include:

- Company fundamentals
- Financial statements
- Valuation metrics
- Analyst recommendations
- Earnings calendars
- Corporate actions
- Institutional holders

This information can be combined with market data to create richer datasets for security analysis and investment research.

---

## 3. Economic Data

Financial markets are strongly influenced by macroeconomic conditions.

The course therefore includes the retrieval and processing of economic indicators such as:

- GDP
- Inflation
- Interest rates

These datasets can be incorporated into market analysis, asset allocation studies, macroeconomic research, and systematic investment models.

---

## 4. Unstructured Data

Not all relevant financial information comes in structured numerical form.

The repository also explores unstructured financial data, particularly:

- Financial news
- Market-related textual information

This creates the foundation for future applications involving:

- Natural Language Processing (NLP)
- Sentiment analysis
- Event detection
- News-based investment signals

---

## 5. Data Quality Checks

Obtaining financial data is only the first step.

Before using any dataset for research or investment analysis, it is important to evaluate its reliability.

The course covers common data-quality issues such as:

- Missing observations
- Duplicate records
- Incorrect timestamps
- Inconsistent frequencies
- Invalid or unexpected values
- Data gaps
- Outliers
- API inconsistencies

Data validation is an essential part of any robust financial data pipeline.

---

## 6. Data Cleaning

Once problems have been identified, the data must be transformed into a consistent and analysis-ready format.

Typical operations include:

- Handling missing values
- Removing duplicates
- Standardizing column names
- Normalizing timestamps
- Converting data types
- Aligning time series
- Adjusting frequencies
- Managing outliers
- Preparing datasets for downstream analysis

The objective is to transform raw financial information into reliable datasets that can be used for quantitative research, visualization, modeling, and portfolio analysis.

---

## Data Pipeline

The general workflow explored throughout the repository can be summarized as:

```text
Introduction
    │
    ▼
Pricing & Market Data
    │
    ├── Equities
    │   ├── Stocks
    │   └── Stock Indices
    │
    ├── FX & Crypto
    │
    └── Derivatives
        ├── Futures
        └── Options
    │
    ▼
Company Data
    │
    ├── Company Fundamentals
    ├── Analyst Recommendations
    ├── Earnings Calendar
    ├── Corporate Actions
    └── Institutional Holders
    │
    ▼
Economic Data
    │
    ├── GDP
    ├── Inflation
    └── Interest Rates
    │
    ▼
Unstructured Data
    │
    └── News
    │
    ▼
Data Quality Checks
    │
    ▼
Data Cleaning


Repository Objectives
```

By completing the material in this repository, the goal is to develop the ability to:

* Retrieve financial data programmatically using Python.
* Work with multiple asset classes and financial datasets.
* Understand the differences between pricing, fundamental, macroeconomic, and unstructured data.
* Interact with financial APIs and data providers.
* Organize raw financial information into consistent data structures.
* Detect common financial data-quality problems.
* Clean and transform datasets for further analysis.
* Build reusable financial data pipelines.
* Prepare data for quantitative finance, portfolio analysis, and investment research applications.

### Technologies

The repository primarily uses:

* Python
* Jupyter Notebook
* pandas
* NumPy
* Financial APIs
* REST APIs
* JSON data
* Time-series data

Additional libraries and data providers may be introduced throughout the course.

### Potential Applications

The techniques covered in this repository can serve as building blocks for more advanced financial applications, including:

* Stock screeners
* Fundamental analysis tools
* Portfolio analytics
* Market dashboards
* Quantitative trading strategies
* Factor models
* Risk analytics
* Macro dashboards
* Event-driven strategies
* News sentiment models
* Financial data pipelines
* Automated investment research

### Learning Approach

This repository is intended to be practical.

Whenever possible, concepts are implemented directly in Python so that the focus remains not only on understanding where financial data comes from, but also on learning how to work with it in real-world applications.

The emphasis is on building reusable workflows rather than isolated code examples.

### Disclaimer

This repository is intended for educational and research purposes only.

The information, code, and examples contained here should not be considered financial or investment advice. Financial data obtained from third-party providers may contain errors, delays, omissions, or licensing restrictions and should always be independently validated before being used in production or investment decision-making.


### Author

Manuel Tellechea

Economist | CMT Charterholder | Quantitative Finance & Investment Research
