with source as (
    select * from {{ source('retail_ai_raw', 'incidents') }}
)
select
    incident_id,
    started_at,
    resolved_at,
    date(started_at) as incident_date,
    severity,
    domain,
    title,
    description,
    affected_component,
    status,
    timestamp_diff(resolved_at, started_at, minute) as resolution_minutes
from source
