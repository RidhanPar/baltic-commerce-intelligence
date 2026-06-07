{{ config(materialized='table') }}

with orders as (
    select * from {{ ref('stg_orders') }}
    where order_status = 'completed'
),
customers as (
    select * from {{ ref('dim_customer') }}
)
select
    c.customer_id,
    c.market,
    c.acquisition_channel,
    min(o.order_date) as first_order_date,
    max(o.order_date) as latest_order_date,
    count(distinct o.order_id) as lifetime_orders,
    sum(o.net_revenue) as lifetime_net_revenue,
    sum(o.contribution_margin) as lifetime_contribution_margin,
    datediff(day, min(o.order_date), max(o.order_date)) as active_span_days
from customers c
left join orders o using (customer_id)
group by c.customer_id, c.market, c.acquisition_channel

