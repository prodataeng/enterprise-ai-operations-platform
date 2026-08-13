with shipments as (

    select *
    from {{ ref('stg_shipments') }}

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
    s.shipment_id,
    s.order_id,
    o.customer_id,
    s.warehouse_id,
    s.shipped_date as date_key,
    o.country_code,
    o.sales_channel,
    s.carrier,
    s.shipped_timestamp,
    s.promised_delivery_timestamp,
    s.delivered_timestamp,
    s.delay_hours,
    s.delivery_status,
    s.is_delayed,
    s.transit_hours
from shipments as s
left join orders as o
    on s.order_id = o.order_id
