with source as (
    select * from {{ source('retail_ai_raw', 'orders') }}
)
select
    order_id,
    customer_id,
    order_timestamp,
    source_available_timestamp,
    date(order_timestamp) as order_date,
    country_code,
    sales_channel,
    order_status,
    item_quantity,
    gross_revenue_sek,
    discount_amount_sek,
    net_revenue_sek,
    vat_amount_sek,
    estimated_cost_sek,
    net_revenue_sek - estimated_cost_sek as estimated_gross_profit_sek,
    timestamp_diff(source_available_timestamp, order_timestamp, minute) as source_delay_minutes,
    order_status = 'completed' as is_completed_order,
    order_status = 'cancelled' as is_cancelled_order
from source
