with pipeline_runs as (

    select *
    from {{ ref('stg_pipeline_runs') }}

)

select
    pipeline_run_id,
    business_date as date_key,
    pipeline_name,
    scheduled_start_timestamp,
    actual_start_timestamp,
    completed_timestamp,
    duration_minutes,
    status,
    error_message,
    is_successful_run,
    is_failed_run,
    is_partial_success_run,
    start_delay_minutes
from pipeline_runs
