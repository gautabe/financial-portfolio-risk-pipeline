# Project Architecture

## Overview

This project follows a layered ELT architecture built with Snowflake and Streamlit.

The objective is to simulate a financial portfolio risk pipeline where raw financial data is ingested, cleaned, enriched, aggregated and exposed through a reporting dashboard.

The architecture is designed around five main layers:

```text
Data Sources
   ↓
RAW Layer
   ↓
SILVER Layer
   ↓
GOLD Layer
   ↓
AUDIT / SECURITY
   ↓
Streamlit Dashboard
```

---

## 1. Data Sources

The source data is generated as CSV files using Python.

Source files:

```text
data/clients.csv
data/instruments.csv
data/market_prices.csv
data/transactions.csv
```

These files simulate a financial services environment with:

* client information;
* financial instruments;
* daily market prices;
* client transactions.

Some invalid transaction records were intentionally added to test data quality rules.

---

## 2. RAW Layer

The RAW layer stores the data as it was ingested from CSV files.

Snowflake schema:

```text
RAW
```

Tables:

```text
RAW.RAW_CLIENTS
RAW.RAW_INSTRUMENTS
RAW.RAW_MARKET_PRICES
RAW.RAW_TRANSACTIONS
```

The purpose of this layer is to preserve the original structure of the source data. Most fields are stored as strings in order to avoid losing information during ingestion.

This layer answers the question:

```text
What did we receive from the source files?
```

---

## 3. SILVER Layer

The SILVER layer applies cleaning, type conversion and enrichment.

Snowflake schema:

```text
SILVER
```

Tables:

```text
SILVER.CLEAN_CLIENTS
SILVER.CLEAN_INSTRUMENTS
SILVER.CLEAN_MARKET_PRICES
SILVER.CLEAN_TRANSACTIONS
SILVER.ENRICHED_POSITIONS
```

Main transformations:

* remove empty client IDs;
* remove invalid transactions;
* convert dates from string to date;
* convert quantities and prices to numeric values;
* remove duplicate transaction IDs;
* standardize transaction side values;
* join transactions with clients;
* join transactions with instruments;
* join transactions with market prices.

The main output of this layer is:

```text
SILVER.ENRICHED_POSITIONS
```

This table contains transaction-level enriched data with business fields such as:

* client segment;
* country;
* risk profile;
* instrument name;
* asset class;
* sector;
* transaction price;
* market close price;
* market value;
* unrealized PnL.

This layer answers the question:

```text
How do we transform raw data into clean and usable data?
```

---

## 4. GOLD Layer

The GOLD layer contains business-ready analytical tables.

Snowflake schema:

```text
GOLD
```

Tables and views:

```text
GOLD.CLIENT_EXPOSURE
GOLD.SEGMENT_PERFORMANCE
GOLD.ASSET_CLASS_EXPOSURE
GOLD.RISK_ALERTS
GOLD.V_CLIENT_EXPOSURE_REPORTING
```

The GOLD layer provides aggregated metrics for reporting and decision-making.

Main outputs:

* total market value by client;
* unrealized PnL by client;
* number of transactions;
* number of instruments;
* exposure by business segment;
* exposure by asset class;
* high exposure alerts;
* high loss alerts.

This layer answers the question:

```text
What insights can the business use?
```

---

## 5. AUDIT Layer

The AUDIT layer stores data quality check results.

Snowflake schema:

```text
AUDIT
```

Table:

```text
AUDIT.DATA_QUALITY_RESULTS
```

Implemented data quality checks:

* missing client ID;
* invalid quantity;
* invalid price;
* duplicate transaction ID;
* unknown instrument symbol.

Each check stores:

* check name;
* source table;
* status;
* number of failed records;
* description;
* execution timestamp.

This layer answers the question:

```text
Can we trust the data before using it for reporting?
```

---

## 6. SECURITY Layer

The SECURITY layer contains governance objects such as masking policies.

Snowflake schema:

```text
SECURITY
```

Security object:

```text
SECURITY.CLIENT_NAME_MASK
```

The masking policy protects sensitive client names by displaying masked values for reporting users:

```text
***MASKED_CLIENT***
```

A dedicated reporting role is used by the dashboard:

```text
REPORTING_ANALYST_ROLE
```

This role can access reporting objects but does not see sensitive client names.

This layer answers the question:

```text
How do we protect sensitive financial client information?
```

---

## 7. Streamlit Dashboard

The dashboard is built with Streamlit and connects to Snowflake using the Snowflake Python connector.

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

The dashboard connects using:

```text
REPORTING_ANALYST_ROLE
```

This ensures that client names are masked in the dashboard.

---

## End-to-End Flow

```text
CSV files
   ↓
RAW tables
   ↓
SILVER clean tables
   ↓
SILVER enriched_positions
   ↓
GOLD analytical tables
   ↓
AUDIT data quality results
   ↓
SECURITY masking policy
   ↓
Streamlit dashboard
```

---

## Design Rationale

The project uses a RAW / SILVER / GOLD architecture because it separates responsibilities clearly:

* RAW preserves original data;
* SILVER cleans and enriches data;
* GOLD prepares data for business reporting;
* AUDIT tracks data quality;
* SECURITY protects sensitive fields;
* Streamlit exposes insights to business users.

This architecture is commonly used in modern data engineering projects because it improves clarity, maintainability, traceability and scalability.
