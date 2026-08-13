select
    warehouse_id,
    city,
    country_code
from {{ source('retail_ai_raw', 'warehouses') }}
