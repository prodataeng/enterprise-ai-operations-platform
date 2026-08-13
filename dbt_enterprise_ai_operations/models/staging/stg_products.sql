with source as (
    select * from {{ source('retail_ai_raw', 'products') }}
)
select
    product_id,
    sku,
    category,
    subcategory,
    list_price_sek,
    unit_cost_sek,
    list_price_sek - unit_cost_sek as unit_margin_sek,
    safe_divide(list_price_sek - unit_cost_sek, list_price_sek) as unit_margin_pct,
    product_type,
    status as product_status
from source
