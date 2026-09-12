"""Streamlit entry point for the ShopSmart sales dashboard."""

from pathlib import Path

import plotly.express as px
import streamlit as st

from data_processing import (
    aggregate_monthly_sales,
    aggregate_sales_by_category,
    aggregate_sales_by_region,
    calculate_total_orders,
    calculate_total_sales,
    load_sales_data,
)

DATA_PATH = Path(__file__).parent / "data" / "sales-data.csv"


@st.cache_data
def get_sales_data(path: str | Path):
    """Cache the validated source data between Streamlit reruns."""
    return load_sales_data(path)


st.set_page_config(page_title="ShopSmart Sales Dashboard", page_icon="📊", layout="wide")
st.title("ShopSmart Sales Dashboard")
st.caption("Executive view of e-commerce sales performance")

try:
    sales_data = get_sales_data(DATA_PATH)
except (FileNotFoundError, OSError, ValueError) as error:
    st.error(f"Sales data could not be loaded: {error}")
    st.stop()

sales_column, orders_column = st.columns(2)
with sales_column:
    st.metric("Total Sales", f"${calculate_total_sales(sales_data):,.2f}")
with orders_column:
    st.metric("Total Orders", f"{calculate_total_orders(sales_data):,}")

monthly_sales = aggregate_monthly_sales(sales_data)
trend_chart = px.line(
    monthly_sales,
    x="month",
    y="sales",
    markers=True,
    title="Sales Trend Over Time",
    labels={"month": "Month", "sales": "Sales ($)"},
)
trend_chart.update_traces(
    hovertemplate="%{x|%b %Y}<br>Sales: $%{y:,.2f}<extra></extra>"
)
st.plotly_chart(trend_chart, use_container_width=True)

category_sales = aggregate_sales_by_category(sales_data)
region_sales = aggregate_sales_by_region(sales_data)

category_chart = px.bar(
    category_sales,
    x="category",
    y="sales",
    title="Sales by Category",
    labels={"category": "Category", "sales": "Sales ($)"},
)
category_chart.update_traces(
    hovertemplate="%{x}<br>Sales: $%{y:,.2f}<extra></extra>"
)

region_chart = px.bar(
    region_sales,
    x="region",
    y="sales",
    title="Sales by Region",
    labels={"region": "Region", "sales": "Sales ($)"},
)
region_chart.update_traces(
    hovertemplate="%{x}<br>Sales: $%{y:,.2f}<extra></extra>"
)

category_column, region_column = st.columns(2)
with category_column:
    st.plotly_chart(category_chart, use_container_width=True)
with region_column:
    st.plotly_chart(region_chart, use_container_width=True)
