-- Customer-level 90-day profitability and repeat-purchase analysis.
with first_orders as (
    select
        customer_id,
        min(order_date) as acquisition_date
    from analytics.fct_orders
    where order_status = 'completed'
    group by customer_id
),
orders_90d as (
    select
        o.customer_id,
        f.acquisition_date,
        o.order_id,
        o.order_date,
        o.market,
        o.acquisition_channel,
        o.net_revenue,
        o.contribution_margin,
        row_number() over (
            partition by o.customer_id
            order by o.order_date, o.order_id
        ) as purchase_number
    from analytics.fct_orders o
    join first_orders f using (customer_id)
    where o.order_status = 'completed'
      and o.order_date < dateadd(day, 90, f.acquisition_date)
),
customer_summary as (
    select
        customer_id,
        acquisition_date,
        market,
        acquisition_channel,
        sum(net_revenue) as revenue_90d,
        sum(contribution_margin) as contribution_margin_90d,
        count(distinct order_id) as orders_90d,
        max(case when purchase_number >= 2 then 1 else 0 end) as repeated_90d
    from orders_90d
    group by customer_id, acquisition_date, market, acquisition_channel
)
select
    date_trunc('month', acquisition_date) as acquisition_month,
    market,
    acquisition_channel,
    count(*) as acquired_customers,
    avg(revenue_90d) as avg_revenue_90d,
    avg(contribution_margin_90d) as avg_contribution_margin_90d,
    avg(repeated_90d) as repeat_purchase_rate_90d,
    percentile_cont(0.5) within group (order by contribution_margin_90d)
        as median_contribution_margin_90d
from customer_summary
group by acquisition_month, market, acquisition_channel
order by acquisition_month, market, acquisition_channel;

