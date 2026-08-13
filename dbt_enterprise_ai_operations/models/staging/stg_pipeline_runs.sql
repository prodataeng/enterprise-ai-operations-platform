with source as (
    select * from {{ source('retail_ai_raw', 'pipeline_runs') }}
)
select
    pipeline_run_id,
    pipeline_name,
    business_date,
    scheduled_start_timestamp,
    actual_start_timestamp,
    completed_timestamp,
    duration_minutes,
    status,
    nullif(error_message, '') as error_message,
    status = 'success' as is_successful_run,
    status = 'failed' as is_failed_run,
    status = 'partial_success' as is_partial_success_run,
    timestamp_diff(actual_start_timestamp, scheduled_start_timestamp, minute) as start_delay_minutes
from source
