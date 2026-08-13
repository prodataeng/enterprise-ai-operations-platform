with warehouses as (

    select *
    from {{ ref('stg_warehouses') }}

)

select
    warehouse_id,
    city,
    country_code
from warehouses
