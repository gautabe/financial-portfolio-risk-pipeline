import os
import random
from datetime import datetime, timedelta

import pandas as pd


# -----------------------------
# Configuration
# -----------------------------

DATA_DIR = "data"
random.seed(42)

os.makedirs(DATA_DIR, exist_ok=True)


# -----------------------------
# Helper functions
# -----------------------------

def generate_business_dates(start_date: str, end_date: str):
    """
    Generate business dates between start_date and end_date.
    Weekends are excluded.
    """
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")

    dates = []
    current = start

    while current <= end:
        if current.weekday() < 5:  # Monday to Friday
            dates.append(current.strftime("%Y-%m-%d"))
        current += timedelta(days=1)

    return dates


# -----------------------------
# 1. Clients
# -----------------------------

clients = [
    ["C001", "NorthBridge Capital", "Wealth Management", "Canada", "Medium"],
    ["C002", "Maple Ridge Fund", "Institutional", "USA", "High"],
    ["C003", "Atlantic Growth Partners", "Investment Management", "UK", "Medium"],
    ["C004", "BlueRiver Family Office", "Wealth Management", "USA", "Low"],
    ["C005", "StoneGate Pension Trust", "Institutional", "Canada", "High"],
    ["C006", "Evergreen Alpha Fund", "Investment Management", "USA", "Medium"],
    ["C007", "Summit Private Wealth", "Wealth Management", "France", "Low"],
    ["C008", "HarborView Capital", "Institutional", "Germany", "High"],
    ["C009", "CedarRock Advisors", "Wealth Management", "Canada", "Medium"],
    ["C010", "IronPeak Asset Management", "Investment Management", "USA", "High"],
]

clients_df = pd.DataFrame(
    clients,
    columns=["client_id", "client_name", "segment", "country", "risk_profile"]
)

clients_df.to_csv(f"{DATA_DIR}/clients.csv", index=False)


# -----------------------------
# 2. Instruments
# -----------------------------

instruments = [
    ["AAPL", "Apple Inc", "Equity", "Technology", "USD", "NASDAQ"],
    ["MSFT", "Microsoft Corp", "Equity", "Technology", "USD", "NASDAQ"],
    ["JPM", "JPMorgan Chase", "Equity", "Financials", "USD", "NYSE"],
    ["GS", "Goldman Sachs Group", "Equity", "Financials", "USD", "NYSE"],
    ["TSLA", "Tesla Inc", "Equity", "Consumer Discretionary", "USD", "NASDAQ"],
    ["NVDA", "NVIDIA Corp", "Equity", "Technology", "USD", "NASDAQ"],
    ["AMZN", "Amazon.com Inc", "Equity", "Consumer Discretionary", "USD", "NASDAQ"],
    ["GOOGL", "Alphabet Inc", "Equity", "Communication Services", "USD", "NASDAQ"],
    ["SPY", "SPDR S&P 500 ETF", "ETF", "Broad Market", "USD", "NYSE"],
    ["TLT", "iShares 20+ Year Treasury Bond ETF", "Bond ETF", "Fixed Income", "USD", "NASDAQ"],
]

instruments_df = pd.DataFrame(
    instruments,
    columns=["symbol", "instrument_name", "asset_class", "sector", "currency", "exchange"]
)

instruments_df.to_csv(f"{DATA_DIR}/instruments.csv", index=False)


# -----------------------------
# 3. Market prices
# -----------------------------

business_dates = generate_business_dates("2026-01-01", "2026-01-31")

base_prices = {
    "AAPL": 185,
    "MSFT": 410,
    "JPM": 170,
    "GS": 390,
    "TSLA": 240,
    "NVDA": 900,
    "AMZN": 180,
    "GOOGL": 150,
    "SPY": 520,
    "TLT": 95,
}

market_price_rows = []

for symbol, base_price in base_prices.items():
    price = base_price

    for date in business_dates:
        daily_change = random.uniform(-0.03, 0.03)
        price = round(price * (1 + daily_change), 2)
        volume = random.randint(1_000_000, 80_000_000)

        market_price_rows.append([
            symbol,
            date,
            price,
            volume
        ])

market_prices_df = pd.DataFrame(
    market_price_rows,
    columns=["symbol", "price_date", "close_price", "volume"]
)

market_prices_df.to_csv(f"{DATA_DIR}/market_prices.csv", index=False)


# -----------------------------
# 4. Transactions
# -----------------------------

transaction_rows = []

client_ids = clients_df["client_id"].tolist()
symbols = instruments_df["symbol"].tolist()
sides = ["BUY", "SELL"]

for i in range(1, 201):
    transaction_id = f"T{i:04d}"
    client_id = random.choice(client_ids)
    symbol = random.choice(symbols)
    trade_date = random.choice(business_dates)

    market_price = market_prices_df[
        (market_prices_df["symbol"] == symbol) &
        (market_prices_df["price_date"] == trade_date)
    ]["close_price"].iloc[0]

    price_variation = random.uniform(-0.02, 0.02)
    trade_price = round(market_price * (1 + price_variation), 2)

    quantity = random.randint(10, 1000)
    side = random.choice(sides)

    transaction_rows.append([
        transaction_id,
        client_id,
        symbol,
        trade_date,
        quantity,
        trade_price,
        side
    ])


# -----------------------------
# 5. Intentional bad records
# These rows will help us test data quality checks later.
# -----------------------------

bad_records = [
    ["T0201", "C001", "AAPL", "2026-01-10", -50, 185.40, "BUY"],       # negative quantity
    ["T0202", "", "MSFT", "2026-01-11", 100, 410.20, "BUY"],          # missing client_id
    ["T0203", "C003", "UNKNOWN", "2026-01-12", 200, 50.00, "BUY"],    # unknown symbol
    ["T0204", "C004", "JPM", "2026-01-13", 120, -170.00, "SELL"],     # negative price
    ["T0001", "C001", "AAPL", "2026-01-02", 100, 185.50, "BUY"],      # duplicate transaction_id
]

transaction_rows.extend(bad_records)

transactions_df = pd.DataFrame(
    transaction_rows,
    columns=["transaction_id", "client_id", "symbol", "trade_date", "quantity", "price", "side"]
)

transactions_df.to_csv(f"{DATA_DIR}/transactions.csv", index=False)


# -----------------------------
# Summary
# -----------------------------

print("CSV files generated successfully!")
print(f"- {DATA_DIR}/clients.csv: {len(clients_df)} rows")
print(f"- {DATA_DIR}/instruments.csv: {len(instruments_df)} rows")
print(f"- {DATA_DIR}/market_prices.csv: {len(market_prices_df)} rows")
print(f"- {DATA_DIR}/transactions.csv: {len(transactions_df)} rows")
print()
print("Note: transactions.csv contains a few intentional bad records for data quality testing.")