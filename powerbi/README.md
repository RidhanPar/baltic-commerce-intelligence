# Power BI Implementation Blueprint

This folder contains a tested analytical model specification and DAX measures, but not a `.pbix` file. That distinction is intentional and stated in the main README.

## Recommended Model

- Dimensions: `dim_prospect`, `dim_customer`, date, market, channel
- Facts: `fct_orders`, `fct_deliveries`, `fct_experiment_assignments`
- Relationships: one-to-many from dimensions to facts; avoid bidirectional relationships by default

## Recommended Pages

1. Executive overview: eligible prospects, conversion, revenue, contribution margin
2. Acquisition economics: conversion and margin per prospect by channel
3. Experiment decision: conversion lift, confidence interval, margin tradeoff
4. Logistics: on-time rate and delivery cost by carrier and market
5. Data trust: reconciliation checks and freshness

Use `measures.dax` as the starting measure layer and the generated CSV marts or SQLite extracts as data sources.
