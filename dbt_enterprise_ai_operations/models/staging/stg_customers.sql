with source as (
    select * from {{ source('retail_ai_raw', 'customers') }}
)
select
    customer_id,
    country_code,
    date(signup_date) as signup_date,
    customer_segment,
    preferred_channel,
    marketing_opt_in,
    age_band
from source
