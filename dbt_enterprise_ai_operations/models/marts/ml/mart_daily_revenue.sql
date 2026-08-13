with daily_orders as (

    select
        date_key,
        country_code,
        sales_channel,

        count(*) as order_count,
        countif(is_completed_order) as completed_order_count,
        countif(is_cancelled_order) as cancelled_order_count,

        sum(
            case
                when is_completed_order then gross_revenue_sek
                else 0
            end
        ) as gross_revenue_sek,

        sum(
            case
                when is_completed_order then discount_amount_sek
                else 0
            end
        ) as discount_amount_sek,

        sum(
            case
                when is_completed_order then net_revenue_sek
                else 0
            end
        ) as net_revenue_sek,

        sum(
            case
                when is_completed_order then estimated_gross_profit_sek
                else 0
            end
        ) as estimated_gross_profit_sek,

        avg(
            case
                when is_completed_order then net_revenue_sek
            end
        ) as average_order_value_sek,

        avg(source_delay_minutes) as avg_source_delay_minutes,
        max(source_delay_minutes) as max_source_delay_minutes

    from {{ ref('fct_orders') }}
    group by 1, 2, 3

)

select *
from daily_orders
