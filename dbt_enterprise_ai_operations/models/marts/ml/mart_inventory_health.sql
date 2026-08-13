with inventory as (

    select
        date_key,
        warehouse_id,
        product_id,
        on_hand_quantity,
        reorder_point,
        below_reorder_point,
        recommended_reorder_quantity,
        is_stockout
    from {{ ref('fct_inventory_snapshots') }}

),

products as (

    select
        product_id,
        category,
        subcategory,
        product_type,
        product_status,
        unit_cost_sek,
        list_price_sek
    from {{ ref('dim_products') }}

)

select
    i.date_key,
    i.warehouse_id,
    i.product_id,
    p.category,
    p.subcategory,
    p.product_type,
    p.product_status,

    i.on_hand_quantity,
    i.reorder_point,
    i.recommended_reorder_quantity,
    i.below_reorder_point,
    i.is_stockout,

    safe_divide(i.on_hand_quantity, nullif(i.reorder_point, 0))
        as stock_to_reorder_ratio,

    i.on_hand_quantity * p.unit_cost_sek
        as inventory_cost_value_sek,

    i.on_hand_quantity * p.list_price_sek
        as inventory_retail_value_sek

from inventory as i
left join products as p
    on i.product_id = p.product_id
