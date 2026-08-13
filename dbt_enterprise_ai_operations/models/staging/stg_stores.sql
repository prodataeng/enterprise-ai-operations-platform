select
    store_id,
    store_name,
    city,
    country_code
from {{ source('retail_ai_raw', 'stores') }}
