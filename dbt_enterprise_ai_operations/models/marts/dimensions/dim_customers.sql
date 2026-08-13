with customers as (

    select *
    from {{ ref('stg_customers') }}

)

select
    customer_id,
    country_code,
    signup_date,
    customer_segment,
    preferred_channel,
    marketing_opt_in,
    age_band
from customers
