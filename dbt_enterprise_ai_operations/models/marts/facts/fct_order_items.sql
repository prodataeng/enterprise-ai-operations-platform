with order_items as (

    select *
    from {{ ref('stg_order_items') }}

),

orders as (

    select
        order_id,
        customer_id,
        order_date,
        country_code,
        sales_channel,
        order_status
    from {{ ref('stg_orders') }}

)

select
    oi.order_item_id,
    oi.order_id,
    o.customer_id,
    oi.product_id,
    o.order_date as date_key,
    o.country_code,
    o.sales_channel,
    o.order_status,
    oi.quantity,
    oi.unit_price_sek,
    oi.discount_pct,
    oi.gross_line_amount_sek,
    oi.discount_amount_sek,
    oi.net_line_amount_sek
from order_items as oi
left join orders as o
    on oi.order_id = o.order_id
