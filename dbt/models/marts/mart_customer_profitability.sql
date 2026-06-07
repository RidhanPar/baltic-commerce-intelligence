with orders as (
    select * from {{ ref('stg_orders') }}
),
customers as (
    select * from {{ ref('stg_customers') }}
)
select
    c.customer_id,
    c.prospect_id,
    c.market,
    c.acquisition_channel,
    min(o.order_date) as first_order_date,
    max(o.order_date) as latest_order_date,
    count(distinct o.order_id) as lifetime_orders,
    round(sum(o.net_revenue), 2) as lifetime_net_revenue,
    round(sum(o.contribution_margin), 2) as lifetime_contribution_margin,
    cast(julianday(max(o.order_date)) - julianday(min(o.order_date)) as integer) as active_span_days
from customers c
left join orders o using (customer_id)
group by c.customer_id, c.prospect_id, c.market, c.acquisition_channel
