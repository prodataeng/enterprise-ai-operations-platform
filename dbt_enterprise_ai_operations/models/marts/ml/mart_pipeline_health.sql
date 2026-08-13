with runs as (

    select *
    from {{ ref('fct_pipeline_runs') }}

)

select
    date_key,
    pipeline_name,
    count(*) as run_count,
    countif(is_successful_run) as successful_run_count,
    countif(is_failed_run) as failed_run_count,
    countif(is_partial_success_run) as partial_success_run_count,

    safe_divide(
        countif(is_successful_run),
        count(*)
    ) as success_rate,

    avg(duration_minutes) as avg_duration_minutes,
    max(duration_minutes) as max_duration_minutes,

    avg(start_delay_minutes) as avg_start_delay_minutes,
    max(start_delay_minutes) as max_start_delay_minutes,

    countif(error_message is not null) as runs_with_errors

from runs
group by 1, 2
