# Excel Finance and Logistics Planning Model

## Workbook Tabs

1. `Instructions`: purpose, owners, refresh steps, definitions.
2. `Parameters`: market, month, FX, fuel-cost scenario, growth assumptions.
3. `Raw_Actuals`: Power Query output from the governed profitability mart.
4. `Raw_Budget`: controlled finance input table.
5. `Variance_Analysis`: actual, budget, variance, variance percentage, driver.
6. `Carrier_Scorecard`: delivery cost, on-time rate, claims, and cost per order.
7. `Scenario_Model`: contribution-margin impact under base, upside, and downside.
8. `Executive_Summary`: pivots, charts, recommendations, and controls.

## Required Excel Skills

- Power Query for refreshable imports and transformation
- Structured tables and named ranges
- `XLOOKUP`, `SUMIFS`, `LET`, `IFERROR`, and dynamic arrays
- Pivot tables, slicers, and conditional formatting
- Data validation for controlled assumptions
- Waterfall chart for budget-to-actual contribution-margin variance
- Reconciliation check that flags any mismatch with Power BI totals

## Control Checks

- Actual totals reconcile to the Snowflake mart.
- Every budget line has an owner and cost category.
- Scenario assumptions stay inside documented bounds.
- No formula errors are present on the executive tab.

