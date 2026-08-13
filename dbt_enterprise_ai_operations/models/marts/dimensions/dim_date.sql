with date_spine as (

    select date_day
    from unnest(
        generate_date_array(
            date('2025-01-01'),
            date('2026-12-31'),
            interval 1 day
        )
    ) as date_day

)

select
    date_day as date_key,
    extract(year from date_day) as year_number,
    extract(quarter from date_day) as quarter_number,
    extract(month from date_day) as month_number,
    format_date('%B', date_day) as month_name,
    extract(week from date_day) as week_number,
    extract(day from date_day) as day_of_month,
    extract(dayofweek from date_day) as day_of_week_number,
    format_date('%A', date_day) as day_name,
    date_trunc(date_day, week(monday)) as week_start_date,
    date_trunc(date_day, month) as month_start_date,
    date_trunc(date_day, quarter) as quarter_start_date,
    date_trunc(date_day, year) as year_start_date,
    extract(dayofweek from date_day) in (1, 7) as is_weekend
from date_spine
