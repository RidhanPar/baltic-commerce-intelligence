-- Portfolio analysis queries. These use the local SQLite warehouse.

-- 1. Rank acquisition channels by contribution margin.
SELECT
    acquisition_channel,
    orders,
    net_revenue,
    contribution_margin,
    contribution_margin_pct,
    RANK() OVER (ORDER BY contribution_margin DESC) AS profitability_rank
FROM mart_channel_profitability
ORDER BY profitability_rank;

-- 2. Find low-cost carriers with a material reliability tradeoff.
SELECT
    market,
    carrier,
    deliveries,
    on_time_rate,
    avg_delivery_cost,
    avg_delivery_cost - AVG(avg_delivery_cost) OVER () AS cost_vs_average,
    on_time_rate - AVG(on_time_rate) OVER () AS reliability_vs_average
FROM mart_logistics
ORDER BY on_time_rate;

-- 3. Compare experiment outcomes using intention-to-treat assignment.
SELECT
    treatment,
    assigned_prospects,
    converted_prospects,
    conversion_rate,
    margin_per_assigned_prospect,
    margin_per_assigned_prospect
        - MAX(CASE WHEN treatment = 'control' THEN margin_per_assigned_prospect END) OVER ()
        AS margin_lift_vs_control
FROM mart_experiment;
