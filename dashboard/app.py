import os

import pandas as pd
import plotly.express as px
import snowflake.connector
import streamlit as st
from dotenv import load_dotenv


# -------------------------------------------------
# Page configuration
# -------------------------------------------------

st.set_page_config(
    page_title="Financial Portfolio Risk Dashboard",
    page_icon="📊",
    layout="wide"
)

load_dotenv()


# -------------------------------------------------
# Snowflake connection
# -------------------------------------------------

@st.cache_resource
def get_connection():
    return snowflake.connector.connect(
        user=os.getenv("SNOWFLAKE_USER"),
        password=os.getenv("SNOWFLAKE_PASSWORD"),
        account=os.getenv("SNOWFLAKE_ACCOUNT"),
        warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
        database=os.getenv("SNOWFLAKE_DATABASE"),
        schema=os.getenv("SNOWFLAKE_SCHEMA"),
        role=os.getenv("SNOWFLAKE_ROLE"),
    )


@st.cache_data(ttl=600)
def run_query(query: str) -> pd.DataFrame:
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(query)
        return cursor.fetch_pandas_all()
    finally:
        cursor.close()


# -------------------------------------------------
# Load data from Snowflake
# -------------------------------------------------

client_exposure = run_query("""
    SELECT *
    FROM GOLD.v_client_exposure_reporting
    ORDER BY total_market_value DESC
""")

segment_performance = run_query("""
    SELECT *
    FROM GOLD.segment_performance
    ORDER BY total_market_value DESC
""")

asset_class_exposure = run_query("""
    SELECT *
    FROM GOLD.asset_class_exposure
    ORDER BY total_market_value DESC
""")

risk_alerts = run_query("""
    SELECT *
    FROM GOLD.risk_alerts
    ORDER BY total_market_value DESC
""")

data_quality = run_query("""
    SELECT *
    FROM AUDIT.data_quality_results
    ORDER BY checked_at DESC
""")


# -------------------------------------------------
# Dashboard title
# -------------------------------------------------

st.title("Financial Portfolio Risk Dashboard")
st.caption(
    "Snowflake ELT pipeline for portfolio exposure, unrealized PnL, risk monitoring and data quality."
)


# -------------------------------------------------
# KPI cards
# -------------------------------------------------

total_market_value = client_exposure["TOTAL_MARKET_VALUE"].sum()
total_pnl = client_exposure["TOTAL_UNREALIZED_PNL"].sum()
number_of_clients = client_exposure["CLIENT_ID"].nunique()
number_of_alerts = risk_alerts.shape[0]

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Market Value", f"${total_market_value:,.2f}")
col2.metric("Total Unrealized PnL", f"${total_pnl:,.2f}")
col3.metric("Number of Clients", number_of_clients)
col4.metric("Risk Alerts", number_of_alerts)


# -------------------------------------------------
# Client exposure
# -------------------------------------------------

st.subheader("Client Exposure")

st.dataframe(
    client_exposure,
    use_container_width=True
)


# -------------------------------------------------
# Segment performance
# -------------------------------------------------

st.subheader("Segment Performance")

fig_segment = px.bar(
    segment_performance,
    x="SEGMENT",
    y="TOTAL_MARKET_VALUE",
    color="COUNTRY",
    title="Total Market Value by Segment and Country"
)

st.plotly_chart(fig_segment, use_container_width=True)


# -------------------------------------------------
# Asset class exposure
# -------------------------------------------------

st.subheader("Asset Class Exposure")

fig_asset = px.pie(
    asset_class_exposure,
    names="ASSET_CLASS",
    values="TOTAL_MARKET_VALUE",
    title="Portfolio Exposure by Asset Class"
)

st.plotly_chart(fig_asset, use_container_width=True)


# -------------------------------------------------
# Risk alerts
# -------------------------------------------------

st.subheader("Risk Alerts")

if risk_alerts.empty:
    st.success("No active risk alerts.")
else:
    st.dataframe(
        risk_alerts,
        use_container_width=True
    )


# -------------------------------------------------
# Data quality
# -------------------------------------------------

st.subheader("Data Quality Results")

st.dataframe(
    data_quality,
    use_container_width=True
)


# -------------------------------------------------
# Footer
# -------------------------------------------------

st.caption(
    "Built with Snowflake, SQL and Streamlit. "
    "Client names are masked through Snowflake governance policies."
)