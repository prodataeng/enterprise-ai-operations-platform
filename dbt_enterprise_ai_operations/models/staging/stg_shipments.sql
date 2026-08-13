with source as (
    select * from {{ source('retail_ai_raw', 'shipments') }}
)
select
    shipment_id,
    order_id,
    warehouse_id,
    carrier,
    shipped_timestamp,
    promised_delivery_timestamp,
    delivered_timestamp,
    date(shipped_timestamp) as shipped_date,
    delay_hours,
    delivery_status,
    delivery_status = 'delayed' as is_delayed,
    timestamp_diff(delivered_timestamp, shipped_timestamp, hour) as transit_hours
from source
