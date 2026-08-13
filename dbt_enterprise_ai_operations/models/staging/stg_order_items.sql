select
    order_item_id,
    order_id,
    product_id,
    quantity,
    unit_price_sek,
    discount_pct,
    gross_line_amount_sek,
    discount_amount_sek,
    net_line_amount_sek
from {{ source('retail_ai_raw', 'order_items') }}
