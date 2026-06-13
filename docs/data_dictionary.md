# Data Dictionary

## Overview

This document describes the main datasets used in the Financial Portfolio Risk Pipeline.

The project uses simulated financial data for clients, instruments, market prices and transactions.

---

## 1. Clients

Source file:

```text
data/clients.csv
```

Snowflake tables:

```text
RAW.RAW_CLIENTS
SILVER.CLEAN_CLIENTS
```

| Column       | Description                | Example             |
| ------------ | -------------------------- | ------------------- |
| client_id    | Unique client identifier   | C001                |
| client_name  | Client or institution name | NorthBridge Capital |
| segment      | Business segment           | Wealth Management   |
| country      | Client country             | Canada              |
| risk_profile | Client risk level          | Medium              |

---

## 2. Instruments

Source file:

```text
data/instruments.csv
```

Snowflake tables:

```text
RAW.RAW_INSTRUMENTS
SILVER.CLEAN_INSTRUMENTS
```

| Column          | Description                 | Example    |
| --------------- | --------------------------- | ---------- |
| symbol          | Financial instrument ticker | AAPL       |
| instrument_name | Full instrument name        | Apple Inc  |
| asset_class     | Type of financial asset     | Equity     |
| sector          | Business sector             | Technology |
| currency        | Trading currency            | USD        |
| exchange        | Market exchange             | NASDAQ     |

---

## 3. Market Prices

Source file:

```text
data/market_prices.csv
```

Snowflake tables:

```text
RAW.RAW_MARKET_PRICES
SILVER.CLEAN_MARKET_PRICES
```

| Column      | Description                 | Example    |
| ----------- | --------------------------- | ---------- |
| symbol      | Financial instrument ticker | AAPL       |
| price_date  | Market price date           | 2026-01-02 |
| close_price | Closing market price        | 188.40     |
| volume      | Daily trading volume        | 53200000   |

---

## 4. Transactions

Source file:

```text
data/transactions.csv
```

Snowflake tables:

```text
RAW.RAW_TRANSACTIONS
SILVER.CLEAN_TRANSACTIONS
```

| Column         | Description                   | Example    |
| -------------- | ----------------------------- | ---------- |
| transaction_id | Unique transaction identifier | T0001      |
| client_id      | Client identifier             | C001       |
| symbol         | Financial instrument ticker   | AAPL       |
| trade_date     | Transaction date              | 2026-01-02 |
| quantity       | Number of units traded        | 100        |
| price          | Transaction price             | 185.50     |
| side           | Transaction type              | BUY        |

---

## 5. Enriched Positions

Snowflake table:

```text
SILVER.ENRICHED_POSITIONS
```

This table joins transactions with clients, instruments and market prices.

| Column            | Description                               |
| ----------------- | ----------------------------------------- |
| transaction_id    | Unique transaction identifier             |
| client_id         | Client identifier                         |
| client_name       | Client name                               |
| segment           | Business segment                          |
| country           | Client country                            |
| risk_profile      | Client risk level                         |
| symbol            | Financial instrument ticker               |
| instrument_name   | Financial instrument name                 |
| asset_class       | Asset class                               |
| sector            | Business sector                           |
| trade_date        | Transaction date                          |
| side              | BUY or SELL                               |
| quantity          | Number of units traded                    |
| transaction_price | Price at transaction time                 |
| close_price       | Market close price                        |
| signed_quantity   | Positive for BUY, negative for SELL       |
| trade_value       | Quantity multiplied by transaction price  |
| market_value      | Quantity multiplied by market close price |
| unrealized_pnl    | Unrealized profit or loss                 |
| processed_at      | Processing timestamp                      |

---

## 6. GOLD Tables

### GOLD.CLIENT_EXPOSURE

Client-level portfolio exposure table.

| Column                 | Description                             |
| ---------------------- | --------------------------------------- |
| client_id              | Client identifier                       |
| client_name            | Client name, masked for reporting users |
| segment                | Business segment                        |
| country                | Client country                          |
| risk_profile           | Client risk level                       |
| number_of_transactions | Total number of transactions            |
| number_of_instruments  | Number of distinct instruments          |
| total_market_value     | Total portfolio market value            |
| total_unrealized_pnl   | Total unrealized profit or loss         |
| risk_alert             | Client risk alert category              |

---

### GOLD.SEGMENT_PERFORMANCE

Aggregated performance by business segment and country.

| Column                 | Description            |
| ---------------------- | ---------------------- |
| segment                | Business segment       |
| country                | Country                |
| number_of_clients      | Number of clients      |
| number_of_transactions | Number of transactions |
| number_of_instruments  | Number of instruments  |
| total_market_value     | Total market value     |
| total_unrealized_pnl   | Total unrealized PnL   |
| avg_unrealized_pnl     | Average unrealized PnL |

---

### GOLD.ASSET_CLASS_EXPOSURE

Portfolio exposure by asset class and sector.

| Column                 | Description               |
| ---------------------- | ------------------------- |
| asset_class            | Financial asset class     |
| sector                 | Business sector           |
| number_of_clients      | Number of clients exposed |
| number_of_transactions | Number of transactions    |
| number_of_symbols      | Number of instruments     |
| total_market_value     | Total market value        |
| total_unrealized_pnl   | Total unrealized PnL      |

---

### GOLD.RISK_ALERTS

Table containing only clients with active risk alerts.

| Column                 | Description                             |
| ---------------------- | --------------------------------------- |
| client_id              | Client identifier                       |
| client_name            | Client name, masked for reporting users |
| segment                | Business segment                        |
| country                | Client country                          |
| risk_profile           | Client risk level                       |
| total_market_value     | Total portfolio market value            |
| total_unrealized_pnl   | Total unrealized PnL                    |
| number_of_transactions | Number of transactions                  |
| number_of_instruments  | Number of instruments                   |
| risk_alert             | Risk alert category                     |
| alert_generated_at     | Alert generation timestamp              |

---

## 7. Audit Table

Snowflake table:

```text
AUDIT.DATA_QUALITY_RESULTS
```

| Column            | Description                       |
| ----------------- | --------------------------------- |
| check_name        | Name of the data quality check    |
| source_table      | Table where the check was applied |
| check_status      | PASSED or FAILED                  |
| failed_records    | Number of records that failed     |
| check_description | Description of the check          |
| checked_at        | Check execution timestamp         |
