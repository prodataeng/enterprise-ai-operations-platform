{% macro evaluate_revenue_forecast_validation(evaluation_start_date='2026-07-01', evaluation_end_date='2026-07-31', horizon=31) %}
    {% set model_name = revenue_ml_model_name('revenue_forecast_arima_validation') %}
    {% set revenue_mart = ref('mart_daily_revenue') %}

    {% set sql %}
        select *
        from ml.evaluate(
            model {{ model_name }},
            (
                select
                    date_key,
                    country_code,
                    sum(net_revenue_sek) as net_revenue_sek
                from {{ revenue_mart }}
                where date_key between date('{{ evaluation_start_date }}')
                                    and date('{{ evaluation_end_date }}')
                group by 1, 2
            ),
            struct(
                {{ horizon }} as horizon,
                true as perform_aggregation
            )
        )
        order by country_code
    {% endset %}

    {% set results = run_query(sql) %}
    {% do log_query_results(results, 'Revenue forecast holdout evaluation') %}
{% endmacro %}
