select
    prospect_id,
    market,
    acquisition_channel,
    cast(engagement_score as real) as engagement_score,
    cast(converted as integer) as converted
from {{ source('raw', 'prospects') }}
