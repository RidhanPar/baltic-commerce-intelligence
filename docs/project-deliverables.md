# Project Deliverables and Recruiter Evaluation

## Completed, Runnable Deliverables

1. Reproducible synthetic prospect-to-order dataset with randomized treatment assignment.
2. Typed SQLite analytical warehouse with primary keys, foreign keys, checks, and reconciliations.
3. Runnable dbt project with staging models, marts, documentation, and tests.
4. Executive HTML dashboard and decision memo.
5. Formatted Excel finance workbook.
6. GitHub Actions workflow running Python and dbt validation.

## Platform Implementation Blueprints

The Power BI/DAX, Snowflake, Databricks, Looker, and R directories demonstrate how the validated model can be implemented in those platforms. They are deliberately separated from completed deliverables so reviewers can distinguish runnable evidence from architectural fluency.

## Reviewer Checklist

| Question | Evidence |
|---|---|
| Can the candidate frame a business decision? | Experiment launch decision and channel budget recommendations |
| Can the candidate avoid vanity metrics? | Conversion lift is evaluated against contribution margin |
| Is the pipeline reproducible? | Fixed seed, one-command run script, generated artifacts |
| Is the data model trustworthy? | Typed tables, constraints, reconciliations, Python and dbt tests |
| Can the candidate communicate? | Dashboard, decision memo, methodology, caveats, interview guide |
| Are platform claims credible? | Runnable core and implementation blueprints are explicitly separated |

## Remaining Production Work

- Replace synthetic sources with governed source-system contracts.
- Add orchestration, observability, ownership, and alerting.
- Validate long-term experiment guardrails and statistical power.
- Implement and validate the selected production BI and cloud platform.
