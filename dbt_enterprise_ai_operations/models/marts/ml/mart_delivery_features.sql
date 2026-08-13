with shipments as (

    select
        shipment_id,
        order_id,
        customer_id,
        warehouse_id,
        date_key,
        country_code,
        sales_channel,
        carrier,
        shipped_timestamp,
        promised_delivery_timestamp,
        delivered_timestamp,
        delay_hours,
        delivery_status,
        is_delayed,
        transit_hours
    from {{ ref('fct_shipments') }}

),

orders as (

    select
        order_id,
        item_quantity,
        net_revenue_sek,
        discount_amount_sek,
        source_delay_minutes
    from {{ ref('fct_orders') }}

)

select
    s.shipment_id,
    s.order_id,
    s.customer_id,
    s.warehouse_id,
    s.date_key,
    s.country_code,
    s.sales_channel,
    s.carrier,

    extract(dayofweek from s.shipped_timestamp) as shipped_day_of_week,
    extract(hour from s.shipped_timestamp) as shipped_hour,
    extract(month from s.shipped_timestamp) as shipped_month,

    o.item_quantity,
    o.net_revenue_sek,
    o.discount_amount_sek,
    o.source_delay_minutes,

    timestamp_diff(
        s.promised_delivery_timestamp,
        s.shipped_timestamp,
        hour
    ) as promised_transit_hours,

    s.transit_hours,
    s.delay_hours,
    s.is_delayed as target_is_delayed

from shipments as s
left join orders as o
    on s.order_id = o.order_id
