with incidents as (

    select *
    from {{ ref('stg_incidents') }}

)

select
    incident_id,
    incident_date as date_key,
    started_at,
    resolved_at,
    severity,
    domain,
    title,
    description,
    affected_component,
    status,
    resolution_minutes
from incidents
