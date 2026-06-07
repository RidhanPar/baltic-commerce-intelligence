# Decision Memo: Profitable Growth and Offer Evaluation

## Executive Decision

Do not launch the free-shipping treatment in its current form. It raises conversion, but the incremental orders do not cover the offer's economics. Protect and scale CRM and Organic Search, and redesign Paid Search around contribution margin rather than conversion.

## Experiment Result

| Metric | Control | Treatment | Difference |
|---|---:|---:|---:|
| Eligible prospects | 3,006 | 2,994 | -12 |
| Conversion rate | 28.74% | 32.50% | +3.76pp |
| Revenue per prospect | EUR 22.51 | EUR 25.40 | +EUR 2.89 |
| Contribution margin per prospect | EUR 0.37 | -EUR 0.71 | -EUR 1.08 |

The conversion lift is statistically significant: 95% CI **+1.43 to +6.09 percentage points**, p=0.0016. The sample-ratio mismatch check is healthy (p=0.8769).

**Interpretation:** The offer attracts incremental buyers and revenue, but the discount and fulfillment economics destroy value. A conversion-only success metric would recommend the wrong decision.

## Acquisition Profitability

| Channel | Prospects | Conversion | Contribution Margin | Margin / Prospect |
|---|---:|---:|---:|---:|
| CRM | 1,031 | 42.67% | EUR 3,496 | EUR 3.39 |
| Organic Search | 1,202 | 39.24% | EUR 2,808 | EUR 2.34 |
| Affiliate | 701 | 32.25% | -EUR 323 | -EUR 0.46 |
| Paid Search | 1,549 | 45.22% | -EUR 3,044 | -EUR 1.97 |
| Paid Social | 1,517 | 29.49% | -EUR 3,966 | -EUR 2.61 |

Paid Search has the highest conversion rate but negative unit economics. CRM combines strong conversion with the highest margin per prospect. Budget decisions should therefore use incremental contribution margin, not volume or conversion in isolation.

## Logistics

FastShip provides the strongest on-time performance across markets, generally above 93%, at a higher average cost. EconomyBox and BalticPost are cheaper but have market-specific reliability gaps. The next operational analysis should quantify whether lower delivery cost offsets refunds, repeat-purchase risk, and support contacts.

## Recommended Actions

1. Redesign the free-shipping treatment with a higher basket threshold or targeted eligibility, then retest against contribution margin per eligible prospect.
2. Protect CRM and Organic Search capacity while testing incremental scale.
3. Rebuild Paid Search bidding and campaign governance around contribution margin; pause segments that cannot demonstrate positive incremental economics.
4. Use carrier-by-market service-level targets rather than selecting one carrier globally.

## Caveats

- All data is synthetic and reproducible; findings demonstrate methodology rather than real-company performance.
- Attribution uses a single acquisition channel.
- Cost allocation and repeat-purchase effects are simplified.
- Statistical inference is appropriate for the generated randomized experiment, but production decisions would also require power planning and longer-term guardrails.
