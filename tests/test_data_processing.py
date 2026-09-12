from pathlib import Path

import pandas as pd
import pytest

from data_processing import (
    aggregate_monthly_sales,
    aggregate_sales_by_category,
    aggregate_sales_by_region,
    calculate_total_orders,
    calculate_total_sales,
    load_sales_data,
    validate_sales_data,
)


def test_load_sales_data_reads_dates_and_numeric_amounts(tmp_path: Path):
    csv_path = tmp_path / "sales.csv"
    csv_path.write_text(
        "date,order_id,product,category,region,quantity,unit_price,total_amount\n"
        "2024-01-15,ORD-1,Headphones,Audio,North,2,25.00,50.00\n",
        encoding="utf-8",
    )

    result = load_sales_data(csv_path)

    assert isinstance(result.loc[0, "date"], pd.Timestamp)
    assert result.loc[0, "total_amount"] == 50.0


def test_validate_sales_data_rejects_missing_required_columns():
    data = pd.DataFrame({"date": ["2024-01-01"], "total_amount": [10.0]})

    with pytest.raises(ValueError, match="Missing required columns"):
        validate_sales_data(data)


def test_load_sales_data_rejects_missing_required_columns(tmp_path: Path):
    csv_path = tmp_path / "incomplete.csv"
    csv_path.write_text("date,total_amount\n2024-01-01,10.00\n", encoding="utf-8")

    with pytest.raises(ValueError, match="Missing required columns"):
        load_sales_data(csv_path)


def test_calculate_total_sales_sums_transaction_amounts():
    data = pd.DataFrame({"total_amount": [10.50, 20.25, 5.25]})

    assert calculate_total_sales(data) == pytest.approx(36.0)


def test_calculate_total_orders_counts_rows():
    data = pd.DataFrame({"order_id": ["ORD-1", "ORD-2", "ORD-3"]})

    assert calculate_total_orders(data) == 3


def test_aggregate_monthly_sales_groups_and_sorts_months():
    data = pd.DataFrame(
        {
            "date": pd.to_datetime(["2024-02-10", "2024-01-15", "2024-02-20"]),
            "total_amount": [20.0, 10.0, 5.0],
        }
    )

    result = aggregate_monthly_sales(data)

    assert list(result["month"].dt.strftime("%Y-%m")) == ["2024-01", "2024-02"]
    assert list(result["sales"]) == [10.0, 25.0]


def test_category_sales_contains_all_categories_sorted_descending():
    data = pd.DataFrame(
        {
            "category": ["Audio", "Electronics", "Audio", "Accessories"],
            "total_amount": [20.0, 100.0, 30.0, 40.0],
        }
    )

    result = aggregate_sales_by_category(data)

    assert list(result["category"]) == ["Electronics", "Audio", "Accessories"]
    assert list(result["sales"]) == [100.0, 50.0, 40.0]


def test_region_sales_contains_all_regions_sorted_descending():
    data = pd.DataFrame(
        {
            "region": ["South", "North", "West", "North"],
            "total_amount": [20.0, 70.0, 30.0, 10.0],
        }
    )

    result = aggregate_sales_by_region(data)

    assert list(result["region"]) == ["North", "West", "South"]
    assert list(result["sales"]) == [80.0, 30.0, 20.0]
