# Interview Pitch — Financial Portfolio Risk Pipeline with Snowflake

## 1. Short Project Summary

I built a Snowflake-based ELT pipeline that simulates a financial portfolio risk monitoring environment.

The pipeline ingests simulated financial data such as clients, instruments, market prices and transactions. The data is loaded into a RAW layer, cleaned and enriched in a SILVER layer, and transformed into business-ready GOLD tables for client exposure, unrealized PnL, segment performance, asset class exposure and risk alerts.

I also implemented data quality checks, an audit table, a masking policy for sensitive client names, and a Streamlit dashboard connected to Snowflake.

---

## 2. Business Problem

The business goal of the project is to help a financial institution monitor portfolio exposure and risk across clients and business segments.

The pipeline answers questions such as:

* Which clients have the highest market exposure?
* Which clients have negative unrealized PnL?
* Which segments have the largest portfolio value?
* Which asset classes represent the largest exposure?
* Are there invalid or suspicious records in the raw transaction data?
* How can sensitive client information be protected for reporting users?

---

## 3. Technical Architecture

The project follows a RAW / SILVER / GOLD data architecture.

The RAW layer stores the original ingested CSV files.

The SILVER layer cleans the data, converts data types, removes invalid records, removes duplicates and joins transactions with clients, instruments and market prices.

The GOLD layer contains aggregated business tables used for reporting and analytics.

I also added an AUDIT layer for data quality results and a SECURITY layer for Snowflake masking policies.

The final output is a Streamlit dashboard connected to Snowflake.

---

## 4. Data Engineering Work Done

In this project, I performed the following tasks:

* generated simulated financial data with Python;
* created Snowflake database, schemas and tables;
* loaded CSV files into Snowflake RAW tables;
* built SILVER transformations using SQL;
* created an enriched positions table;
* calculated trade value, market value and unrealized PnL;
* created GOLD analytical tables;
* implemented data quality checks;
* stored audit results in a dedicated AUDIT schema;
* created a Snowflake masking policy;
* tested governed access with a reporting analyst role;
* connected Streamlit to Snowflake;
* built a business-facing dashboard.

---

## 5. Data Quality Checks

I intentionally added some bad records in the raw transaction file in order to test the quality rules.

The implemented checks detect:

* missing client IDs;
* invalid quantities;
* invalid prices;
* duplicate transaction IDs;
* unknown financial instrument symbols.

The results are stored in:

```text
AUDIT.DATA_QUALITY_RESULTS
```

This makes the pipeline more transparent and easier to monitor.

---

## 6. Security and Governance

Because this project simulates a financial services environment, I added a governance layer.

I created a Snowflake masking policy on the client name column. When the dashboard connects using the reporting analyst role, client names are masked as:

```text
***MASKED_CLIENT***
```

This simulates column-level security for sensitive client information.

---

## 7. Streamlit Dashboard

The Streamlit dashboard displays:

* total market value;
* total unrealized PnL;
* number of clients;
* number of risk alerts;
* client exposure;
* segment performance;
* asset class exposure;
* risk alerts;
* data quality results.

The dashboard connects to Snowflake using a reporting role, so sensitive client names remain masked.

---

## 8. Interview Explanation

A strong way to explain the project in an interview:

“I built a Snowflake-based ELT pipeline inspired by a financial services risk monitoring use case. The pipeline ingests simulated client, transaction, instrument and market price data into a RAW layer. Then I clean and standardize the data in a SILVER layer, where I handle type conversion, invalid records and duplicates. After that, I create an enriched positions table by joining transactions with clients, instruments and market prices.

From there, I build GOLD tables for client exposure, segment performance, asset class exposure and risk alerts. I also implemented data quality checks and stored the results in an audit table. To simulate governance in a banking environment, I added a Snowflake masking policy on client names and tested it using a reporting analyst role. Finally, I connected a Streamlit dashboard to Snowflake to visualize exposure, PnL, risk alerts and data quality results.”

---

## 9. What I Would Improve Next

Future improvements could include:

* orchestrating the pipeline with Airflow;
* using dbt for transformations and testing;
* adding Snowflake Tasks for scheduled refreshes;
* adding incremental loading with Streams;
* adding more advanced risk metrics;
* deploying the Streamlit dashboard;
* adding CI/CD with GitHub Actions;
* adding automated tests for SQL transformations.
