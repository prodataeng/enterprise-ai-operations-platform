with orders as (

    select *
    from {{ ref('stg_orders') }}

)

select
    order_id,
    customer_id,
    order_date as date_key,
    order_timestamp,
    source_available_timestamp,
    country_code,
    sales_channel,
    order_status,
    item_quantity,
    gross_revenue_sek,
    discount_amount_sek,
    net_revenue_sek,
    vat_amount_sek,
    estimated_cost_sek,
    estimated_gross_profit_sek,
    source_delay_minutes,
    is_completed_order,
    is_cancelled_order
from orders
