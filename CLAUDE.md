# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project commands

Create the local environment and install dependencies on Windows PowerShell:

```powershell
python -m venv venv
.\venv\Scripts\python.exe -m pip install -r requirements.txt
```

Run the dashboard locally:

```powershell
.\venv\Scripts\python.exe -m streamlit run app.py
```

Run the complete test suite:

```powershell
.\venv\Scripts\python.exe -m pytest -q
```

Run one test or one test group:

```powershell
.\venv\Scripts\python.exe -m pytest tests/test_data_processing.py::test_calculate_total_sales_sums_transaction_amounts -v
.\venv\Scripts\python.exe -m pytest tests/test_data_processing.py -k "category or region" -v
```

Check formatting-related whitespace errors and repository status:

```powershell
git diff --check
git status
```

## Architecture

This is a small Streamlit analytics dashboard for the ShopSmart e-commerce dataset.

- `app.py` is the Streamlit entry point. It configures the page, loads the repository-relative CSV, renders KPI metrics, builds the Plotly monthly trend chart, and renders category and region bar charts.
- `data_processing.py` is the calculation boundary. It validates and normalizes CSV data, calculates KPI values, and returns sorted aggregation DataFrames. Keep these operations outside Streamlit code so they remain unit-testable.
- `tests/test_data_processing.py` tests the data-processing boundary with small in-memory DataFrames and temporary CSV files.
- `data/sales-data.csv` is the supplied source dataset. The application expects the required date, order, product, category, region, quantity, unit-price, and total-amount columns.
- `TASKS.md` is the durable milestone board. Keep milestone status, acceptance criteria, implementation commit hashes, and Notes lines synchronized with the Git history.
- `docs/superpowers/specs/` contains the approved product design, and `docs/superpowers/plans/` contains the implementation plan that maps engineering steps to TASK IDs.

The dashboard uses monthly aggregation for the executive sales trend. Category and regional aggregations are sorted from highest to lowest sales before Plotly renders them. The app catches file and validation errors and displays a Streamlit error instead of continuing with incomplete data.

## Project conventions

- Use the plain `venv/` environment and `requirements.txt`; do not introduce uv or conda files.
- Use repository-relative paths derived from `Path(__file__).parent`; do not add machine-specific absolute paths.
- Keep Phase 2 features out of this release: authentication, database integration, exports, alerts, filters, drill-down, and mobile-specific enhancements.
- Keep `venv/`, Python caches, and Streamlit secrets ignored by Git.
- Include the applicable `TASK-*` milestone ID in implementation commit messages.
- Deployment is a human-executed step from merged `main`; do not deploy, authenticate, or handle credentials automatically.

## Lessons

- Verify both automated calculations and the running Streamlit page; unit tests do not prove chart ordering or visual presentation.
- Keep data validation before column-specific conversions when possible so incomplete CSV files produce a clear user-facing error rather than a raw `KeyError`.
- Record the code commit hash—not the later board-update commit—on each milestone's `Commit:` line in `TASKS.md`.
