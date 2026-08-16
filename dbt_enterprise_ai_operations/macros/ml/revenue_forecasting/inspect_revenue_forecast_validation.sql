{% macro inspect_revenue_forecast_validation(show_all_candidate_models=false) %}
    {% set model_name = revenue_ml_model_name('revenue_forecast_arima_validation') %}

    {% set sql %}
        select *
        from ml.arima_evaluate(
            model {{ model_name }},
            struct({{ 'true' if show_all_candidate_models else 'false' }} as show_all_candidate_models)
        )
        order by country_code
    {% endset %}

    {% set results = run_query(sql) %}
    {% do log_query_results(results, 'ARIMA diagnostics') %}
{% endmacro %}
