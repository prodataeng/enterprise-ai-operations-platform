{% macro train_revenue_forecast_validation(training_end_date='2026-06-30', horizon=31) %}
    {% set model_name = revenue_ml_model_name('revenue_forecast_arima_validation') %}
    {% set revenue_mart = ref('mart_daily_revenue') %}

    {% set sql %}
        create or replace model {{ model_name }}
        options (
            model_type = 'ARIMA_PLUS',
            time_series_timestamp_col = 'date_key',
            time_series_data_col = 'net_revenue_sek',
            time_series_id_col = 'country_code',
            data_frequency = 'DAILY',
            horizon = {{ horizon }},
            decompose_time_series = true,
            holiday_region = 'EMEA'
        ) as
        select
            date_key,
            country_code,
            sum(net_revenue_sek) as net_revenue_sek
        from {{ revenue_mart }}
        where date_key <= date('{{ training_end_date }}')
        group by 1, 2
    {% endset %}

    {% do log('Training validation revenue forecast model: ' ~ model_name, info=true) %}
    {% do run_query(sql) %}
    {% do log('Validation model training completed.', info=true) %}
{% endmacro %}
