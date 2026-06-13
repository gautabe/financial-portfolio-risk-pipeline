# Financial Portfolio Risk Pipeline with Snowflake

## Project Overview

This project is a Snowflake-based ELT pipeline that simulates a financial services portfolio risk environment.

The goal is to ingest, clean, transform and analyze financial portfolio data in order to monitor client exposure, unrealized profit and loss, portfolio concentration, risk alerts and data quality.

This project was designed as a Data Engineering portfolio project inspired by a banking and investment management environment. All data used in this project is simulated and does not represent real client or internal company data.

---

## Business Context

Financial institutions need reliable data pipelines to monitor portfolio exposure, client-level risk, market value and trading activity.

This project simulates a scenario where a financial institution wants to track:

* client portfolio exposure;
* market value by client;
* unrealized profit and loss;
* exposure by business segment;
* exposure by asset class;
* high-risk clients;
* data quality issues in raw transaction data;
* sensitive client information through governance controls.

---

## Tech Stack

* Snowflake
* SQL
* Python
* Pandas
* Streamlit
* Plotly
* Snowflake Connector for Python
* Git / GitHub

---

## Architecture

The project follows a layered data architecture:

```text
CSV Files
   ↓
Snowflake RAW Layer
   ↓
Snowflake SILVER Layer
   ↓
SILVER Enriched Positions
   ↓
Snowflake GOLD Layer
   ↓
AUDIT and SECURITY Layers
   ↓
Streamlit Dashboard
```

---

## Data Layers

### RAW Layer

The RAW layer stores the ingested CSV data close to its original structure.

Tables:

```text
RAW.RAW_CLIENTS
RAW.RAW_INSTRUMENTS
RAW.RAW_MARKET_PRICES
RAW.RAW_TRANSACTIONS
```

In this layer, most columns are stored as strings to preserve the original format of the source files.

---

### SILVER Layer

The SILVER layer cleans, standardizes and enriches the raw data.

Tables:

```text
SILVER.CLEAN_CLIENTS
SILVER.CLEAN_INSTRUMENTS
SILVER.CLEAN_MARKET_PRICES
SILVER.CLEAN_TRANSACTIONS
SILVER.ENRICHED_POSITIONS
```

Main transformations:

* trimming text fields;
* converting dates;
* converting numeric fields;
* removing invalid transactions;
* removing duplicate transaction IDs;
* joining transactions with clients, instruments and market prices;
* calculating trade value;
* calculating market value;
* calculating unrealized PnL.

---

### GOLD Layer

The GOLD layer contains business-ready analytical tables used by the dashboard.

Tables and views:

```text
GOLD.CLIENT_EXPOSURE
GOLD.SEGMENT_PERFORMANCE
GOLD.ASSET_CLASS_EXPOSURE
GOLD.RISK_ALERTS
GOLD.V_CLIENT_EXPOSURE_REPORTING
```

Main metrics:

* total market value;
* total unrealized PnL;
* number of clients;
* number of transactions;
* number of instruments;
* exposure by client;
* exposure by business segment;
* exposure by asset class;
* risk alerts.

---

## Data Quality and Audit

The project includes a dedicated audit layer to track data quality checks.

Table:

```text
AUDIT.DATA_QUALITY_RESULTS
```

Implemented checks:

* missing client ID;
* invalid quantity;
* invalid price;
* duplicate transaction ID;
* unknown financial instrument symbol.

The audit layer helps provide traceability and shows which records failed quality checks before being used for business reporting.

---

## Security and Governance

A masking policy was implemented in Snowflake to protect sensitive client names.

Security object:

```text
SECURITY.CLIENT_NAME_MASK
```

The masking policy hides client names for reporting users and displays masked values such as:

```text
***MASKED_CLIENT***
```

A reporting role was also created:

```text
REPORTING_ANALYST_ROLE
```

This role is used by the Streamlit dashboard to simulate governed access to reporting data.

---

## Streamlit Dashboard

The project includes a Streamlit dashboard connected to Snowflake.

Dashboard file:

```text
dashboard/app.py
```

The dashboard displays:

* total market value;
* total unrealized PnL;
* number of clients;
* number of risk alerts;
* client exposure table;
* segment performance chart;
* asset class exposure chart;
* risk alerts table;
* data quality results.

Client names are masked in the dashboard through Snowflake governance policies.

---

## Project Structure

```text
financial-portfolio-risk-pipeline/
│
├── README.md
├── requirements.txt
├── .env.example
├── .gitignore
│
├── data/
│   ├── clients.csv
│   ├── transactions.csv
│   ├── instruments.csv
│   └── market_prices.csv
│
├── sql/
│   ├── 01_create_database.sql
│   ├── 02_create_raw_tables.sql
│   ├── 03_load_raw_data.sql
│   ├── 04_silver_transformations.sql
│   ├── 05_gold_transformations.sql
│   └── 06_data_quality_checks.sql
│
├── src/
│   └── generate_sample_data.py
│
├── dashboard/
│   └── app.py
│
└── docs/
    ├── architecture.md
    ├── data_dictionary.md
    └── interview_pitch.md
```

---

## How to Run the Project

### 1. Clone the repository

```bash
git clone <repository-url>
cd financial-portfolio-risk-pipeline
```

### 2. Create a virtual environment

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Create a `.env` file

Create a `.env` file at the root of the project using the structure below:

```env
SNOWFLAKE_USER=your_username
SNOWFLAKE_PASSWORD=your_password
SNOWFLAKE_ACCOUNT=your_account_identifier
SNOWFLAKE_WAREHOUSE=ETL_WH
SNOWFLAKE_DATABASE=MS_PORTFOLIO_DB
SNOWFLAKE_SCHEMA=GOLD
SNOWFLAKE_ROLE=REPORTING_ANALYST_ROLE
```

The `.env` file must not be committed to GitHub.

### 5. Run the Streamlit dashboard

```bash
streamlit run dashboard/app.py
```

---

## Key Results

The final dashboard provides a business-friendly view of portfolio risk and exposure.

Main outputs include:

* total market value across all clients;
* total unrealized PnL;
* client-level exposure;
* risk alerts for high exposure and high loss;
* segment-level performance;
* asset class exposure;
* data quality monitoring results;
* masked client names for governed reporting.

---

## What I Learned

Through this project, I practiced:

* designing a Snowflake ELT pipeline;
* building RAW, SILVER and GOLD data layers;
* loading CSV data into Snowflake;
* writing SQL transformations;
* implementing data quality checks;
* creating audit tables;
* applying Snowflake masking policies;
* creating a secure reporting view;
* connecting Streamlit to Snowflake;
* building a business-facing risk dashboard.

---

## Disclaimer

This project uses simulated financial data for educational and portfolio purposes only. It is not connected to Morgan Stanley or any real financial institution.
