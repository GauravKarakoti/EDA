# End-to-End Exploratory Data Analysis (EDA) — Retail Transactions

A portfolio-ready, reproducible Python EDA project using a **synthetic retail transactions dataset** (2,512 rows before cleaning, with intentionally introduced missing values, duplicates, and quantity anomalies).

## Project goals
- Inspect raw data and profile data quality.
- Clean data with documented, reproducible rules.
- Explore sales, profit, customer, product, category, region, and time trends.
- Detect outliers and examine numeric relationships.
- Export publication-ready figures, cleaned data, and a concise HTML report.

## Quick start

```bash
# 1. Create and activate a virtual environment
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the complete pipeline
python main.py
```

Outputs are written to:
- `data/processed/cleaned_retail_transactions.csv`
- `reports/figures/` — PNG charts
- `reports/eda_report.html` — self-contained summary report

## Dataset
`data/raw/retail_transactions.csv` is synthetic and generated with a fixed random seed. It is suitable for demonstrating EDA techniques but **must not be represented as real company data**. The raw file deliberately includes duplicate rows, missing values, and unusually high quantities so the cleaning and quality checks have something to identify.

## Cleaning decisions
1. Parse `order_date` as a date.
2. Remove exact duplicate rows.
3. Impute missing `region` and `payment_method` with their modes.
4. Impute missing `discount` with the median.
5. Flag quantity values above the 99th percentile for review; preserve them in the cleaned dataset and report rather than deleting them automatically.
6. Recalculate `net_sales` and `profit_margin` from the available business fields, where possible.

## Repository structure

```text
end_to_end_eda/
├── data/
│   ├── raw/retail_transactions.csv
│   └── processed/
├── notebooks/eda_walkthrough.ipynb
├── reports/figures/
├── src/
│   ├── data_loader.py
│   ├── data_cleaning.py
│   ├── analysis.py
│   └── visualization.py
├── main.py
├── requirements.txt
└── README.md
```

## Suggested portfolio extensions
- Replace the sample CSV with a public dataset while retaining the pipeline.
- Add unit tests for cleaning functions.
- Add a Streamlit dashboard.
- Add cohort retention and customer lifetime value analysis.
- Add a predictive model only after the EDA questions and target variable are clearly defined.
