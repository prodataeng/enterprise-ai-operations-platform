with source as (
    select * from {{ source('retail_ai_raw', 'payments') }}
)
select
    payment_id,
    order_id,
    payment_method,
    payment_status,
    payment_amount_sek,
    payment_timestamp,
    date(payment_timestamp) as payment_date,
    payment_status = 'pending' as is_pending_payment,
    payment_status = 'captured' as is_captured_payment,
    payment_status = 'refunded' as is_refunded_payment
from source
