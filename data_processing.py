"""Data loading, validation, and aggregation helpers for the dashboard."""

from pathlib import Path

import pandas as pd

REQUIRED_COLUMNS = {
    "date",
    "order_id",
    "product",
    "category",
    "region",
    "quantity",
    "unit_price",
    "total_amount",
}


def validate_sales_data(dataframe: pd.DataFrame) -> None:
    """Validate the columns and core values required by the dashboard."""
    missing_columns = sorted(REQUIRED_COLUMNS - set(dataframe.columns))
    if missing_columns:
        raise ValueError(f"Missing required columns: {', '.join(missing_columns)}")

    if dataframe.empty:
        raise ValueError("The sales data file contains no records")

    required_values = dataframe[
        ["date", "order_id", "product", "category", "region", "quantity", "unit_price", "total_amount"]
    ]
    if required_values.isna().any().any():
        raise ValueError("The sales data contains missing required values")

    if (dataframe["total_amount"] < 0).any() or (dataframe["quantity"] < 0).any():
        raise ValueError("The sales data contains negative values")


def load_sales_data(path: str | Path) -> pd.DataFrame:
    """Load, normalize, and validate sales data from a CSV file."""
    dataframe = pd.read_csv(path)
    missing_columns = sorted(REQUIRED_COLUMNS - set(dataframe.columns))
    if missing_columns:
        raise ValueError(f"Missing required columns: {', '.join(missing_columns)}")

    dataframe["date"] = pd.to_datetime(dataframe["date"], errors="coerce")
    for column in ("quantity", "unit_price", "total_amount"):
        dataframe[column] = pd.to_numeric(dataframe[column], errors="coerce")

    validate_sales_data(dataframe)
    return dataframe


def calculate_total_sales(dataframe: pd.DataFrame) -> float:
    """Return the total transaction value."""
    return float(dataframe["total_amount"].sum())


def calculate_total_orders(dataframe: pd.DataFrame) -> int:
    """Return the number of transaction records."""
    return int(len(dataframe))


def aggregate_monthly_sales(dataframe: pd.DataFrame) -> pd.DataFrame:
    """Aggregate transaction value by calendar month in chronological order."""
    monthly = (
        dataframe.assign(month=dataframe["date"].dt.to_period("M").dt.to_timestamp())
        .groupby("month", as_index=False)["total_amount"]
        .sum()
        .rename(columns={"total_amount": "sales"})
        .sort_values("month")
        .reset_index(drop=True)
    )
    return monthly


def _aggregate_sales(dataframe: pd.DataFrame, group_column: str) -> pd.DataFrame:
    """Aggregate transaction value by a categorical column."""
    return (
        dataframe.groupby(group_column, as_index=False)["total_amount"]
        .sum()
        .rename(columns={"total_amount": "sales"})
        .sort_values("sales", ascending=False)
        .reset_index(drop=True)
    )


def aggregate_sales_by_category(dataframe: pd.DataFrame) -> pd.DataFrame:
    """Aggregate sales by product category from highest to lowest."""
    return _aggregate_sales(dataframe, "category")


def aggregate_sales_by_region(dataframe: pd.DataFrame) -> pd.DataFrame:
    """Aggregate sales by region from highest to lowest."""
    return _aggregate_sales(dataframe, "region")
