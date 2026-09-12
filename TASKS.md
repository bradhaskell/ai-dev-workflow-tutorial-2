# ShopSmart Sales Dashboard: Tasks

This file tracks all work for the e-commerce sales dashboard.
Each milestone moves through To Do -> In Progress -> Done.

## Definition of Done

The following must be true before any milestone moves to Done:

- Acceptance criteria are met
- The app runs locally with `streamlit run app.py`
- Changes are committed with the milestone ID in the commit message

## To Do

## In Progress

## Done

- [x] **TASK-1: Environment setup and data loading**
  - [x] Project uses a plain Python virtual environment in `venv/` and dependencies are listed in `requirements.txt`
  - [x] App runs with `streamlit run app.py`, shows a dashboard title, and loads `data/sales-data.csv`
  - [x] Missing or invalid data is handled with a clear user-facing message
  - Commit: b096b0f
  - Notes: Added a repository-relative loader, validation, requirements, and ignored local environment files.

- [x] **TASK-2: KPI cards**
  - [x] Total Sales is displayed prominently with currency formatting
  - [x] Total Orders is displayed prominently with number formatting
  - Commit: 60f90ab
  - Notes: KPI calculations and formatted Streamlit metric cards are implemented and verified against the supplied dataset.

- [x] **TASK-3: Sales trend chart**
  - [x] An interactive line chart shows sales over time at the approved granularity
  - [x] The chart uses the correct date and sales values from the CSV data
  - Commit: 7a8aa12
  - Notes: Monthly aggregation and Plotly hover formatting are implemented.

- [x] **TASK-4: Category and regional breakdowns**
  - [x] A bar chart shows sales for every product category, sorted highest to lowest
  - [x] A bar chart shows sales for every region, sorted highest to lowest
  - [x] Both charts provide clear labels and interactive tooltips
  - Commit: 2a182d9
  - Notes: Category and region aggregations are sorted descending and rendered as labeled Plotly bar charts.

- [x] **TASK-5: Testing and refinement**
  - [x] Data calculations are isolated in a separate module with pytest coverage
  - [x] The test suite passes without errors
  - [x] The complete dashboard meets the PRD acceptance criteria and has a professional presentation
  - Commit: 263d69a
  - Notes: Added project memory, strengthened data validation, rejected invalid numeric values, and cached validated data; local smoke test returned HTTP 200 with clean startup output.

- [x] **TASK-6: Deployment to Streamlit Community Cloud**
  - [x] The completed dashboard is deployed from the merged `main` branch
  - [x] The public Streamlit URL loads without errors
  - [x] The live URL is recorded in this file and near the top of `README.md`
  - Commit:
  - Notes: Deployed from the merged `main` branch to Streamlit Community Cloud at https://ai-dev-workflow-tutorial-2-qkuvthm5nljvkg9ojsxk73.streamlit.app/. Verified in a private/incognito browser window: the dashboard loads with the ShopSmart title, Total Sales and Total Orders KPIs, the monthly sales trend chart, and the category and region breakdowns, with no errors.
