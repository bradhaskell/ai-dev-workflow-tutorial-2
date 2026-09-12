# ShopSmart Sales Dashboard Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build, test, review, and prepare a public Streamlit sales dashboard from the supplied ShopSmart CSV data, with deployment handed off to the student after the feature branch is merged into `main`.

**Architecture:** `app.py` owns Streamlit configuration, page layout, KPI rendering, and Plotly charts. `data_processing.py` owns CSV loading, validation, calculations, and aggregations, with those behaviors covered by focused pytest tests in `tests/`. The app uses repository-relative data paths, a plain `venv/` virtual environment, and dependencies listed in `requirements.txt`.

**Tech Stack:** Python 3.11+, Streamlit, Pandas, Plotly, pytest, Git, Streamlit Community Cloud.

**Spec:** `docs/superpowers/specs/2026-09-11-sales-dashboard-design.md`

## Global Constraints

- Work on the current `feature/sales-dashboard` branch; do not create or use a Git worktree.
- Use a plain Python virtual environment in `venv/`; do not use uv or conda.
- List runtime and test dependencies in `requirements.txt`.
- Keep data calculations in `data_processing.py`, separate from Streamlit UI code.
- Use the repository-relative source path `data/sales-data.csv`; never use an absolute local path.
- Use monthly sales aggregation for the executive trend chart.
- Sort category and region sales from highest to lowest.
- Handle missing, unreadable, malformed, or incomplete data with a clear user-facing Streamlit message.
- Keep Phase 2 features out of scope: authentication, database integration, exports, alerts, filters, drill-down, and mobile-specific enhancements.
- Do not deploy automatically; deployment is the student’s final step from merged `main`.
- Include the applicable milestone ID in every implementation commit message.
- Do not commit `venv/`, Python caches, or other generated local artifacts.

---

### Task 1: Project scaffold and safe data loading (TASK-1)

**Files:**
- Create: `app.py`
- Create: `data_processing.py`
- Create: `requirements.txt`
- Create: `.gitignore`
- Create: `tests/__init__.py`
- Create: `tests/test_data_processing.py`
- Use: `data/sales-data.csv`

**Interfaces:**
- Produces `load_sales_data(path: str | Path) -> pandas.DataFrame`.
- Produces `validate_sales_data(dataframe: pandas.DataFrame) -> None`, raising a clear `ValueError` for missing required columns or invalid required values.
- `app.py` consumes `load_sales_data("data/sales-data.csv")` and catches expected loading/validation errors before rendering dependent content.

- [ ] **Step 1: Create the plain dependency list**

Create `requirements.txt` with the packages required by the application and tests:

```text
streamlit
pandas
plotly
pytest
```

- [ ] **Step 2: Create the repository ignore rules**

Create `.gitignore` containing at least:

```text
venv/
__pycache__/
.pytest_cache/
*.py[cod]
.streamlit/secrets.toml
```

- [ ] **Step 3: Create the failing loader and validation tests**

Add tests that define the required behavior before implementation:

```python
from pathlib import Path

import pandas as pd
import pytest

from data_processing import load_sales_data, validate_sales_data


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
```

- [ ] **Step 4: Run the focused tests to verify they fail**

Run:

```powershell
python -m pytest tests/test_data_processing.py -v
```

Expected: FAIL because `data_processing.py` and its functions do not exist yet.

- [ ] **Step 5: Implement loading and validation**

Create `data_processing.py` with a required-column set containing:

```python
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
```

`load_sales_data` should read the CSV with Pandas, parse `date` using `pd.to_datetime(..., errors="coerce")`, convert `quantity`, `unit_price`, and `total_amount` with numeric coercion, reject invalid required values, call `validate_sales_data`, and return the validated DataFrame. `validate_sales_data` should raise `ValueError("Missing required columns: ...")` when columns are absent and a clear `ValueError` when required date or numeric values are invalid.

- [ ] **Step 6: Implement the initial Streamlit entry point**

Create `app.py` that:

```python
from pathlib import Path

import streamlit as st

from data_processing import load_sales_data

DATA_PATH = Path(__file__).parent / "data" / "sales-data.csv"

st.set_page_config(page_title="ShopSmart Sales Dashboard", layout="wide")
st.title("ShopSmart Sales Dashboard")

try:
    sales_data = load_sales_data(DATA_PATH)
except (FileNotFoundError, OSError, ValueError) as error:
    st.error(f"Sales data could not be loaded: {error}")
    st.stop()

st.success(f"Loaded {len(sales_data):,} sales transactions.")
```

- [ ] **Step 7: Run the focused tests again**

Run:

```powershell
python -m pytest tests/test_data_processing.py -v
```

Expected: PASS for the loader and validation tests.

- [ ] **Step 8: Create and install the local virtual environment**

Run on Windows PowerShell:

```powershell
python -m venv venv
.\venv\Scripts\python.exe -m pip install -r requirements.txt
```

- [ ] **Step 9: Run the initial dashboard locally**

Run:

```powershell
.\venv\Scripts\python.exe -m streamlit run app.py
```

Expected: The page opens without a traceback, shows the ShopSmart title, and reports that 482 transactions were loaded. Stop the server with `Ctrl+C` after checking it.

- [ ] **Step 10: Commit TASK-1**

Run:

```powershell
git add app.py data_processing.py requirements.txt .gitignore tests
 git commit -m "TASK-1: set up project and data loading"
```

The commit must not contain `venv/`.

---

### Task 2: KPI calculations and scorecards (TASK-2)

**Files:**
- Modify: `data_processing.py`
- Modify: `app.py`
- Modify: `tests/test_data_processing.py`

**Interfaces:**
- Produces `calculate_total_sales(dataframe: pandas.DataFrame) -> float`.
- Produces `calculate_total_orders(dataframe: pandas.DataFrame) -> int`.
- `app.py` consumes both functions and renders `st.metric` cards.

- [ ] **Step 1: Add failing KPI tests**

Append tests:

```python
from data_processing import calculate_total_orders, calculate_total_sales


def test_calculate_total_sales_sums_transaction_amounts():
    data = pd.DataFrame({"total_amount": [10.50, 20.25, 5.25]})

    assert calculate_total_sales(data) == pytest.approx(36.0)


def test_calculate_total_orders_counts_rows():
    data = pd.DataFrame({"order_id": ["ORD-1", "ORD-2", "ORD-3"]})

    assert calculate_total_orders(data) == 3
```

- [ ] **Step 2: Run the KPI tests and confirm failure**

Run:

```powershell
.\venv\Scripts\python.exe -m pytest tests/test_data_processing.py -k "total_sales or total_orders" -v
```

Expected: FAIL because the calculation functions are not yet defined.

- [ ] **Step 3: Implement the KPI calculations**

Add:

```python
def calculate_total_sales(dataframe: pd.DataFrame) -> float:
    return float(dataframe["total_amount"].sum())


def calculate_total_orders(dataframe: pd.DataFrame) -> int:
    return int(len(dataframe))
```

- [ ] **Step 4: Run the KPI tests and confirm success**

Run:

```powershell
.\venv\Scripts\python.exe -m pytest tests/test_data_processing.py -k "total_sales or total_orders" -v
```

Expected: PASS.

- [ ] **Step 5: Add the KPI cards to the dashboard**

Import the calculation functions in `app.py`, compute the values after loading data, and render:

```python
from data_processing import calculate_total_orders, calculate_total_sales

col_sales, col_orders = st.columns(2)
with col_sales:
    st.metric("Total Sales", f"${calculate_total_sales(sales_data):,.2f}")
with col_orders:
    st.metric("Total Orders", f"{calculate_total_orders(sales_data):,}")
```

- [ ] **Step 6: Run tests and inspect the KPI layout**

Run:

```powershell
.\venv\Scripts\python.exe -m pytest
.\venv\Scripts\python.exe -m streamlit run app.py
```

Expected: Tests pass and the dashboard shows approximately `$116,500` and `482` in prominent KPI cards. Stop the server after inspection.

- [ ] **Step 7: Commit TASK-2**

Run:

```powershell
git add app.py data_processing.py tests/test_data_processing.py
git commit -m "TASK-2: add KPI scorecards"
```

---

### Task 3: Monthly sales trend chart (TASK-3)

**Files:**
- Modify: `data_processing.py`
- Modify: `app.py`
- Modify: `tests/test_data_processing.py`

**Interfaces:**
- Produces `aggregate_monthly_sales(dataframe: pandas.DataFrame) -> pandas.DataFrame` with columns `month` and `sales`.
- The returned `month` values are chronological and `sales` values are numeric.
- `app.py` consumes the result to create a Plotly line chart.

- [ ] **Step 1: Add a failing monthly-aggregation test**

Append:

```python
from data_processing import aggregate_monthly_sales


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
```

- [ ] **Step 2: Run the focused test and confirm failure**

Run:

```powershell
.\venv\Scripts\python.exe -m pytest tests/test_data_processing.py::test_aggregate_monthly_sales_groups_and_sorts_months -v
```

Expected: FAIL because `aggregate_monthly_sales` does not exist.

- [ ] **Step 3: Implement monthly aggregation**

Add:

```python
def aggregate_monthly_sales(dataframe: pd.DataFrame) -> pd.DataFrame:
    monthly = (
        dataframe.assign(month=dataframe["date"].dt.to_period("M").dt.to_timestamp())
        .groupby("month", as_index=False)["total_amount"]
        .sum()
        .rename(columns={"total_amount": "sales"})
        .sort_values("month")
        .reset_index(drop=True)
    )
    return monthly
```

- [ ] **Step 4: Run the focused test and confirm success**

Run:

```powershell
.\venv\Scripts\python.exe -m pytest tests/test_data_processing.py::test_aggregate_monthly_sales_groups_and_sorts_months -v
```

Expected: PASS.

- [ ] **Step 5: Render the Plotly line chart**

In `app.py`, import `plotly.express as px` and `aggregate_monthly_sales`, then add:

```python
monthly_sales = aggregate_monthly_sales(sales_data)
trend_chart = px.line(
    monthly_sales,
    x="month",
    y="sales",
    markers=True,
    title="Sales Trend Over Time",
    labels={"month": "Month", "sales": "Sales ($)"},
)
trend_chart.update_traces(hovertemplate="%{x|%b %Y}<br>Sales: $%{y:,.2f}<extra></extra>")
st.plotly_chart(trend_chart, use_container_width=True)
```

- [ ] **Step 6: Run tests and inspect the trend chart**

Run:

```powershell
.\venv\Scripts\python.exe -m pytest
.\venv\Scripts\python.exe -m streamlit run app.py
```

Expected: The dashboard shows one chronological monthly line chart with interactive tooltips and no errors. Stop the server after inspection.

- [ ] **Step 7: Commit TASK-3**

Run:

```powershell
git add app.py data_processing.py tests/test_data_processing.py
git commit -m "TASK-3: add monthly sales trend chart"
```

---

### Task 4: Category and regional breakdown charts (TASK-4)

**Files:**
- Modify: `data_processing.py`
- Modify: `app.py`
- Modify: `tests/test_data_processing.py`

**Interfaces:**
- Produces `aggregate_sales_by_category(dataframe: pandas.DataFrame) -> pandas.DataFrame` with columns `category` and `sales`, descending by `sales`.
- Produces `aggregate_sales_by_region(dataframe: pandas.DataFrame) -> pandas.DataFrame` with columns `region` and `sales`, descending by `sales`.
- `app.py` consumes both results to render Plotly bar charts.

- [ ] **Step 1: Add failing category and region sorting tests**

Append:

```python
from data_processing import aggregate_sales_by_category, aggregate_sales_by_region


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
```

- [ ] **Step 2: Run the focused tests and confirm failure**

Run:

```powershell
.\venv\Scripts\python.exe -m pytest tests/test_data_processing.py -k "category or region" -v
```

Expected: FAIL because the aggregation functions do not exist.

- [ ] **Step 3: Implement sorted category and region aggregations**

Add:

```python
def _aggregate_sales(dataframe: pd.DataFrame, group_column: str) -> pd.DataFrame:
    return (
        dataframe.groupby(group_column, as_index=False)["total_amount"]
        .sum()
        .rename(columns={"total_amount": "sales"})
        .sort_values("sales", ascending=False)
        .reset_index(drop=True)
    )


def aggregate_sales_by_category(dataframe: pd.DataFrame) -> pd.DataFrame:
    return _aggregate_sales(dataframe, "category").rename(columns={"category": "category"})


def aggregate_sales_by_region(dataframe: pd.DataFrame) -> pd.DataFrame:
    return _aggregate_sales(dataframe, "region").rename(columns={"region": "region"})
```

The public functions must return exactly the column names used by the chart code and tests.

- [ ] **Step 4: Run the focused tests and confirm success**

Run:

```powershell
.\venv\Scripts\python.exe -m pytest tests/test_data_processing.py -k "category or region" -v
```

Expected: PASS.

- [ ] **Step 5: Render both Plotly bar charts**

In `app.py`, compute both aggregations and render them in two columns:

```python
category_sales = aggregate_sales_by_category(sales_data)
region_sales = aggregate_sales_by_region(sales_data)

category_chart = px.bar(
    category_sales,
    x="category",
    y="sales",
    title="Sales by Category",
    labels={"category": "Category", "sales": "Sales ($)"},
)
category_chart.update_traces(hovertemplate="%{x}<br>Sales: $%{y:,.2f}<extra></extra>")

region_chart = px.bar(
    region_sales,
    x="region",
    y="sales",
    title="Sales by Region",
    labels={"region": "Region", "sales": "Sales ($)"},
)
region_chart.update_traces(hovertemplate="%{x}<br>Sales: $%{y:,.2f}<extra></extra>")

category_column, region_column = st.columns(2)
with category_column:
    st.plotly_chart(category_chart, use_container_width=True)
with region_column:
    st.plotly_chart(region_chart, use_container_width=True)
```

- [ ] **Step 6: Run all tests and inspect both charts**

Run:

```powershell
.\venv\Scripts\python.exe -m pytest
.\venv\Scripts\python.exe -m streamlit run app.py
```

Expected: All tests pass; five categories and four regions are shown; both charts are sorted highest to lowest and provide tooltips. Stop the server after inspection.

- [ ] **Step 7: Commit TASK-4**

Run:

```powershell
git add app.py data_processing.py tests/test_data_processing.py
git commit -m "TASK-4: add category and region breakdowns"
```

---

### Task 5: Full testing, refinement, project memory, and branch review (TASK-5)

**Files:**
- Modify: `tests/test_data_processing.py` as needed for defects found during verification
- Modify: `app.py` or `data_processing.py` only for verified defects
- Create: `CLAUDE.md`
- Modify: `TASKS.md`

**Interfaces:**
- The complete application must satisfy the PRD acceptance criteria.
- `CLAUDE.md` must document run/test commands, file responsibilities, data location, and a Lessons section.
- `TASKS.md` must move completed implementation milestones to Done with checked criteria, code commit hashes, and Notes lines.

- [ ] **Step 1: Run the complete automated test suite**

Run:

```powershell
.\venv\Scripts\python.exe -m pytest -q
```

Expected: All tests pass.

- [ ] **Step 2: Perform a clean local dashboard verification**

Stop any existing Streamlit process, then run:

```powershell
.\venv\Scripts\python.exe -m streamlit run app.py
```

Inspect the page manually against the PRD. Confirm the title, KPI values, monthly trend, all categories, all regions, descending bar order, labels, tooltips, and professional layout. Stop the server after verification.

- [ ] **Step 3: Fix only verified defects**

For each defect, add or update a focused test when the behavior is calculation-related, make the smallest implementation change, rerun the focused test, then rerun the full suite and local app. Do not add Phase 2 features.

- [ ] **Step 4: Verify repository hygiene**

Run:

```powershell
git status --short
git diff --check
git check-ignore -v venv .pytest_cache
```

Expected: no unintended changes, no whitespace errors, and generated directories are ignored.

- [ ] **Step 5: Generate project memory**

Run Claude Code’s initialization command:

```text
/init
```

Read `CLAUDE.md` and correct inaccurate commands or paths. It must explain:

```text
- Activate or directly invoke the venv Python on Windows.
- Run the app with python -m streamlit run app.py.
- Run tests with python -m pytest.
- app.py owns Streamlit UI and charts.
- data_processing.py owns loading, validation, and calculations.
- data/sales-data.csv is the source dataset.
```

- [ ] **Step 6: Add lessons from the task board**

Add a `## Lessons` section to `CLAUDE.md`. Include rules based on actual Notes entries, such as verifying chart sort order visually and keeping calculations outside Streamlit UI code. Do not invent lessons that did not arise during the work.

- [ ] **Step 7: Commit project memory**

Run:

```powershell
git add CLAUDE.md
git commit -m "Add project memory (CLAUDE.md)"
```

- [ ] **Step 8: Update implementation milestones on the board**

For each completed implementation milestone, move the entry from `To Do` to `Done`, check every acceptance criterion, record the hash of the last code commit for that milestone on its `Commit:` line, and add a `Notes:` line. Keep TASK-6 in To Do because deployment is deliberately deferred until after merging.

- [ ] **Step 9: Commit the board update**

Run:

```powershell
git add TASKS.md
git commit -m "TASK-5: mark implementation milestones complete"
```

- [ ] **Step 10: Run the branch code review**

Run Claude Code’s review command:

```text
/code-review feature/sales-dashboard
```

If findings are valid, fix them on this branch, rerun tests, locally verify the app, and commit with:

```powershell
git add app.py data_processing.py tests CLAUDE.md TASKS.md
git commit -m "TASK-5: address branch review findings"
```

Leave findings that are outside the PRD scope only after documenting the decision in the milestone Notes.

- [ ] **Step 11: Confirm a clean branch and push it**

Run:

```powershell
git status
git branch --show-current
git log --oneline --decorate --graph --all
git push -u origin feature/sales-dashboard
```

Expected: the branch is clean, the feature branch is pushed, and implementation commits contain TASK-1 through TASK-5 identifiers.

---

### Task 6: Human deployment handoff and public URL bookkeeping (TASK-6)

**Files:**
- Modify: `TASKS.md` after deployment
- Modify: `README.md` after deployment

**Interfaces:**
- Deployment consumes the merged `main` branch, `app.py`, `requirements.txt`, and `data/sales-data.csv`.
- Produces a public Streamlit Community Cloud URL.
- The student, not an automated agent, performs authentication, authorization, and deployment.

- [ ] **Step 1: Merge the reviewed branch into main**

After the branch review is resolved, request a no-fast-forward merge:

```text
Merge feature/sales-dashboard into main with a merge commit and no fast-forward. Do not deploy yet.
```

Then verify and push:

```powershell
git switch main
git pull --ff-only origin main
git push origin main
```

- [ ] **Step 2: Deploy manually from main**

Open `https://share.streamlit.io`, sign in with GitHub, and create a public app configured as:

```text
Repository: your GitHub repository
Branch: main
Main file path: app.py
```

Wait for the build to complete and record the exact public URL. Do not place credentials, tokens, or private data in the repository.

- [ ] **Step 3: Verify the public application**

Open the public URL in a private/incognito browser window. Confirm it loads the same KPIs, line chart, category chart, and region chart as the local app. If deployment fails, inspect the Streamlit build logs and correct only repository issues such as missing dependencies or incorrect paths.

- [ ] **Step 4: Record the deployment URL**

Update `TASKS.md` so TASK-6 is in Done, every deployment criterion is checked, the exact URL is recorded, and a `Notes:` line explains the successful public verification. Add the same URL near the top of `README.md`.

- [ ] **Step 5: Commit and push the final board**

Run:

```powershell
git add TASKS.md README.md
git commit -m "TASK-6: record deployed dashboard URL"
git push origin main
```

- [ ] **Step 6: Perform final evidence verification**

Run:

```powershell
git status
git log --oneline --decorate --graph --all
git log --oneline -- TASKS.md
```

Confirm the repository contains the PRD, task board, design spec, implementation plan, `CLAUDE.md`, source code, tests, requirements, and final deployment URL. Confirm `main` is clean and pushed.
