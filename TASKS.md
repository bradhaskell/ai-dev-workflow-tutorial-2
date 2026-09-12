# ShopSmart Sales Dashboard: Tasks

This file tracks all work for the e-commerce sales dashboard.
Each milestone moves through To Do -> In Progress -> Done.

## Definition of Done

The following must be true before any milestone moves to Done:

- Acceptance criteria are met
- The app runs locally with `streamlit run app.py`
- Changes are committed with the milestone ID in the commit message

## To Do

- [ ] **TASK-1: Environment setup and data loading**
  - [ ] Project uses a plain Python virtual environment in `venv/` and dependencies are listed in `requirements.txt`
  - [ ] App runs with `streamlit run app.py`, shows a dashboard title, and loads `data/sales-data.csv`
  - [ ] Missing or invalid data is handled with a clear user-facing message
  - Commit:

- [ ] **TASK-2: KPI cards**
  - [ ] Total Sales is displayed prominently with currency formatting
  - [ ] Total Orders is displayed prominently with number formatting
  - Commit:

- [ ] **TASK-3: Sales trend chart**
  - [ ] An interactive line chart shows sales over time at the approved granularity
  - [ ] The chart uses the correct date and sales values from the CSV data
  - Commit:

- [ ] **TASK-4: Category and regional breakdowns**
  - [ ] A bar chart shows sales for every product category, sorted highest to lowest
  - [ ] A bar chart shows sales for every region, sorted highest to lowest
  - [ ] Both charts provide clear labels and interactive tooltips
  - Commit:

- [ ] **TASK-5: Testing and refinement**
  - [ ] Data calculations are isolated in a separate module with pytest coverage
  - [ ] The test suite passes without errors
  - [ ] The complete dashboard meets the PRD acceptance criteria and has a professional presentation
  - Commit:

- [ ] **TASK-6: Deployment to Streamlit Community Cloud**
  - [ ] The completed dashboard is deployed from the merged `main` branch
  - [ ] The public Streamlit URL loads without errors
  - [ ] The live URL is recorded in this file and near the top of `README.md`
  - Commit:

## In Progress

## Done
