select
    order_id, customer_id, prospect_id, order_date, market, acquisition_channel,
    cast(net_revenue as real) as net_revenue,
    cast(contribution_margin as real) as contribution_margin
from {{ source('raw', 'orders') }}
