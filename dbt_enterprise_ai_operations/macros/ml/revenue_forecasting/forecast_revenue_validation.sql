{% macro forecast_revenue_validation(horizon=31, confidence_level=0.95) %}
    {% set model_name = revenue_ml_model_name('revenue_forecast_arima_validation') %}

    {% set sql %}
        select
            country_code,
            date(forecast_timestamp) as forecast_date,
            forecast_value,
            prediction_interval_lower_bound,
            prediction_interval_upper_bound,
            confidence_level
        from ml.forecast(
            model {{ model_name }},
            struct(
                {{ horizon }} as horizon,
                {{ confidence_level }} as confidence_level
            )
        )
        order by country_code, forecast_date
    {% endset %}

    {% set results = run_query(sql) %}
    {% do log_query_results(results, 'Validation forecast') %}
{% endmacro %}
