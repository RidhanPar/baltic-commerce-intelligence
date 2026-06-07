# Resume and Interview Guide

## Resume Project Entry

**Baltic Commerce Intelligence | End-to-End Analytics Case Study**

- Built a reproducible commerce analytics platform using Python, SQL, dbt, SQLite, Excel, and GitHub Actions, including a typed warehouse, 18 automated tests, and generated executive reporting.
- Evaluated a randomized offer across 6,000 eligible prospects, identifying a statistically significant +3.76pp conversion lift but a EUR 1.08 decline in contribution margin per prospect.
- Modeled acquisition, refunds, and delivery costs to identify profitable CRM and Organic Search growth and expose a high-conversion but loss-making Paid Search channel.

## Two-Minute Interview Story

**Situation:** A commerce leadership team wants growth, but conversion, acquisition spend, delivery performance, and profitability are reported separately.

**Task:** Build a trusted analytical model and decide where to invest and whether to launch a promotional offer.

**Action:** I created a deterministic synthetic source system, modeled eligible prospects through purchase and fulfillment, built a typed SQLite warehouse and runnable dbt project, added quality and reconciliation tests, and produced statistical experiment evidence, an executive dashboard, and an Excel finance workbook.

**Result:** The treatment raised conversion significantly but reduced margin per prospect, so I recommended redesign rather than launch. The channel analysis also showed that the highest-converting channel was loss-making, changing the recommended acquisition strategy.

## Strong Interview Discussion Points

- Why intention-to-treat analysis starts with all eligible assigned prospects, including non-buyers.
- Why statistical significance does not imply commercial value.
- How primary keys, foreign keys, typed fields, reconciliations, and CI create trust.
- Why margin per prospect is more decision-relevant than conversion or revenue alone.
- How the same semantic model can be implemented in Power BI, Snowflake, Databricks, and Looker.

## Honest Positioning

- State clearly that the data is synthetic.
- Describe Python, SQLite, SQL, dbt, Excel, dashboard, and CI components as runnable and validated.
- Describe Power BI/DAX, Snowflake, Databricks, Looker, and R components as implementation blueprints unless you separately deploy and validate them.
