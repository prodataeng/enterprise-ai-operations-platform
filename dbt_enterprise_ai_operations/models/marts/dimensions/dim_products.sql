with products as (

    select *
    from {{ ref('stg_products') }}

)

select
    product_id,
    sku,
    category,
    subcategory,
    list_price_sek,
    unit_cost_sek,
    unit_margin_sek,
    unit_margin_pct,
    product_type,
    product_status
from products
