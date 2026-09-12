# ShopSmart Sales Dashboard Design

## Context and goals

ShopSmart needs a self-service sales dashboard that gives finance, marketing, regional, and executive stakeholders immediate visibility into sales performance. The Phase 1 release will replace recurring manual spreadsheet reporting with a public Streamlit dashboard backed by the supplied CSV dataset.

The dashboard must satisfy the PRD acceptance criteria while remaining simple enough to understand and maintain. Phase 2 features—including authentication, database integration, exports, alerts, filtering, transaction drill-down, and mobile-specific enhancements—are explicitly out of scope.

## Users and primary questions

- Finance stakeholders need Total Sales and Total Orders at a glance.
- Marketing stakeholders need sales by product category.
- Regional stakeholders need sales by geographic region.
- Executive stakeholders need to understand sales movement over time.

## User interface

The Streamlit page will use a clear executive-oriented layout:

1. A ShopSmart sales-dashboard title and short context subtitle.
2. A KPI row with prominently formatted Total Sales and Total Orders metrics.
3. A full-width interactive sales-trend line chart.
4. Two side-by-side interactive bar charts: sales by category and sales by region.

Plotly will provide interactive tooltips and consistent chart labeling. Category and region charts will display every value present in the dataset and sort bars from highest sales to lowest sales.

The sales trend will use monthly aggregation because the source covers twelve months and the intended audience is management reviewing an executive-level view. Dates will be displayed in chronological order and sales will be shown as the y-axis measure.

## Data flow and architecture

The repository-relative source file is `data/sales-data.csv`. `app.py` will own Streamlit page configuration, layout, and chart rendering. A separate data-processing module will own data loading, validation, calculations, and aggregation so those behaviors can be tested without starting Streamlit.

The data-processing interface will provide focused functions for:

- Loading and validating the CSV.
- Computing total sales.
- Counting total orders.
- Aggregating monthly sales.
- Aggregating sales by category in descending order.
- Aggregating sales by region in descending order.

The implementation will use Pandas for tabular operations and Plotly for visualizations. A plain Python virtual environment in `venv/` will be used for local development, and dependencies will be declared in `requirements.txt`. No uv, conda, database, or external service is required for the application itself.

## Validation and error handling

The loader will validate that the expected source columns are available, including date, order identifier, category, region, and transaction amount fields. Dates and numeric values will be converted or validated before calculations run.

If the CSV is missing, unreadable, malformed, or missing required columns, the application will show a clear user-facing Streamlit error and stop rendering dependent dashboard content. The app will use the repository-relative path so it works both locally and on Streamlit Community Cloud; it will not depend on an absolute Windows path.

## Testing strategy

Pytest tests will cover the calculation and aggregation behaviors in the data-processing module, including:

- Total sales equals the sum of transaction amounts.
- Total orders reflects the transaction records.
- Monthly sales uses valid chronological date grouping.
- Category and region aggregations include all values and sort descending by sales.
- Invalid or incomplete data is rejected clearly where practical.

Chart rendering and Streamlit layout will be verified through local execution and manual browser inspection because those UI behaviors are not meaningfully covered by unit tests alone.

## Operational and quality requirements

The application should load quickly for the supplied dataset, use readable Python, keep responsibilities separated, and provide clear labels suitable for an executive presentation. The repository must exclude `venv/`, Python caches, and other generated local artifacts through `.gitignore`.

The completed implementation will be tested locally, reviewed on `feature/sales-dashboard`, and merged into `main` with a no-fast-forward merge commit. Deployment is intentionally a human-executed final handoff: after the merge and push to `main`, the student will deploy the app through Streamlit Community Cloud and record the public URL in `TASKS.md` and `README.md`.

## Success criteria

The design is successful when the implementation can demonstrate:

- Visible Total Sales and Total Orders KPIs.
- A correct interactive monthly sales-trend line chart.
- Correct descending category and regional sales bar charts.
- Correct calculations from `data/sales-data.csv`.
- Passing automated tests for data calculations.
- A clear, professional, error-free local dashboard.
- A deployable application using `requirements.txt` and `app.py`.
