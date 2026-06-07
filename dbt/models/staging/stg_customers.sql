select customer_id, prospect_id, market, acquisition_channel, acquisition_date
from {{ source('raw', 'customers') }}
