with inventory as (

    select *
    from {{ ref('stg_inventory_snapshots') }}

)

select
    snapshot_date as date_key,
    warehouse_id,
    product_id,
    on_hand_quantity,
    reorder_point,
    below_reorder_point,
    recommended_reorder_quantity,
    is_stockout
from inventory
