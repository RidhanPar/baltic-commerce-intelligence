# Decision Memo: Profitable Growth Opportunities

## Executive Summary

The generated data supports three actions:

1. Reallocate acquisition investment away from Paid Social toward Organic Search and CRM.
2. Investigate or reroute EconomyBox deliveries where service quality matters.
3. Redesign the free-shipping treatment before considering launch.

## Acquisition Profitability

| Channel | Orders | Net Revenue | Contribution Margin | Margin Rate |
|---|---:|---:|---:|---:|
| Organic Search | 836 | €48,115 | €6,628 | 13.8% |
| CRM | 702 | €38,537 | €5,178 | 13.4% |
| Paid Search | 1,067 | €60,383 | €207 | 0.3% |
| Affiliate | 463 | €24,725 | -€326 | -1.3% |
| Paid Social | 823 | €44,845 | -€6,613 | -14.8% |

**Interpretation:** Paid Social creates substantial revenue but destroys contribution margin after its higher acquisition cost and other variable costs are included. Revenue-only reporting would hide this problem.

## Logistics Performance

| Carrier | Deliveries | On-Time Rate | Average Delivery Cost |
|---|---:|---:|---:|
| FastShip | 1,304 | 95.8% | €5.52 |
| BalticPost | 1,738 | 91.6% | €4.58 |
| EconomyBox | 849 | 78.5% | €3.97 |

**Interpretation:** EconomyBox is cheapest, but its reliability gap is material. A route-level analysis should determine whether the savings justify the customer-experience risk.

## Experiment Result

The generated treatment cohort has lower margin per assigned customer than control. Because every generated customer places at least one order, conversion is not an informative endpoint in this starter experiment; the meaningful measure is contribution margin per assigned customer.

**Decision:** Do not launch. Redesign the experiment so the treatment can influence conversion and repeat purchase, then evaluate both commercial lift and statistical uncertainty.

## Caveats

- All data is synthetic and intentionally contains business patterns to discover.
- Attribution uses the customer acquisition channel rather than a multi-touch model.
- Shared costs use simplified order-level allocation.
- The experiment module demonstrates intention-to-treat logic but is not a production experiment.

