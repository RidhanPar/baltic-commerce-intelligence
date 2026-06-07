# Synthetic Data Methodology

## Purpose

The dataset is synthetic so the full project can be published and reproduced without exposing private company data. It is designed to create realistic analytical uncertainty, not to prove a predetermined commercial conclusion.

## Design Principles

- **Prospects may not convert.** The experiment population includes both buyers and non-buyers.
- **Outcomes emerge from interactions.** Conversion depends on channel intent, market, device, engagement, treatment, and random noise.
- **Profitability is not a single hardcoded channel ranking.** It depends on acquisition cost, repeat behavior, category mix, market pricing, refunds, discounts, and delivery costs.
- **Logistics performance varies by route and season.** Carrier performance interacts with market, category, peak season, and random variation.
- **Experiment assignment is randomized.** Treatment modestly affects conversion and discounts, creating a real tradeoff between growth and unit economics.

## Known Simplifications

- Attribution uses the acquisition channel rather than a multi-touch model.
- Shared costs use simplified order-level allocation.
- Customer behavior is simulated rather than learned from historical data.
- The experiment is designed for portfolio demonstration, not production launch approval.

## Reproducibility

The generator uses a fixed random seed by default. Changing `--seed` produces a new valid scenario and helps test whether recommendations remain stable.
