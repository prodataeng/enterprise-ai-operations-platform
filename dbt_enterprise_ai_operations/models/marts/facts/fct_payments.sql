with payments as (

    select *
    from {{ ref('stg_payments') }}

),

orders as (

    select
        order_id,
        customer_id,
        country_code,
        sales_channel
    from {{ ref('stg_orders') }}

)

select
    p.payment_id,
    p.order_id,
    o.customer_id,
    p.payment_date as date_key,
    o.country_code,
    o.sales_channel,
    p.payment_method,
    p.payment_status,
    p.payment_amount_sek,
    p.payment_timestamp,
    p.is_pending_payment,
    p.is_captured_payment,
    p.is_refunded_payment
from payments as p
left join orders as o
    on p.order_id = o.order_id
