select
    p.acquisition_channel,
    count(*) as prospects,
    sum(p.converted) as converted_prospects,
    round(avg(p.converted), 4) as conversion_rate,
    round(sum(coalesce(o.contribution_margin, 0)), 2) as contribution_margin
from {{ ref('stg_prospects') }} p
left join {{ ref('stg_orders') }} o using (prospect_id)
group by p.acquisition_channel
