{% macro detect_revenue_anomalies(
    anomaly_prob_threshold=0.99
) %}

    {% set model_name =
        revenue_ml_model_name('revenue_forecast_arima')
    %}

    {% set revenue_mart =
        ref('mart_daily_revenue')
    %}

    {% set sql %}

        select
            country_code,
            date(date_key) as anomaly_date,
            net_revenue_sek as actual_revenue,
            lower_bound,
            upper_bound,
            anomaly_probability,

            case
                when net_revenue_sek < lower_bound then 'LOW'
                when net_revenue_sek > upper_bound then 'HIGH'
                else 'NORMAL'
            end as anomaly_direction

        from ml.detect_anomalies(
            model {{ model_name }},

            struct(
                {{ anomaly_prob_threshold }}
                as anomaly_prob_threshold
            ),

            (
                select
                    date_key,
                    country_code,
                    sum(net_revenue_sek) as net_revenue_sek
                from {{ revenue_mart }}
                group by
                    date_key,
                    country_code
            )
        )

        where is_anomaly = true

        order by
            anomaly_probability desc,
            country_code,
            anomaly_date

        limit 50

    {% endset %}

    {% set results = run_query(sql) %}

    {% do log_query_results(
        results,
        'Revenue anomalies'
    ) %}

{% endmacro %}