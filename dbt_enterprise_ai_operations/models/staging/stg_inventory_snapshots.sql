select
    snapshot_date,
    warehouse_id,
    product_id,
    on_hand_quantity,
    reorder_point,
    below_reorder_point,
    recommended_reorder_quantity,
    on_hand_quantity = 0 as is_stockout
from {{ source('retail_ai_raw', 'inventory_snapshots') }}
