{% macro evaluate_delivery_delay_validation(
    test_start_date='2026-06-01',
    test_end_date='2026-07-31',
    threshold=0.5
) %}

    {% set model_name =
        delivery_delay_model_name('delivery_delay_logistic_validation')
    %}

    {% set feature_mart =
        ref('mart_delivery_features')
    %}

    {% set sql %}

        select
            precision,
            recall,
            accuracy,
            f1_score,
            log_loss,
            roc_auc

        from ml.evaluate(
            model {{ model_name }},

            (
                select
                    warehouse_id,
                    country_code,
                    sales_channel,
                    carrier,
                    shipped_day_of_week,
                    shipped_hour,
                    shipped_month,
                    item_quantity,
                    net_revenue_sek,
                    discount_amount_sek,
                    source_delay_minutes,
                    promised_transit_hours,
                    target_is_delayed

                from {{ feature_mart }}

                where date_key between
                    date('{{ test_start_date }}')
                    and date('{{ test_end_date }}')
            ),

            struct(
                {{ threshold }} as threshold
            )
        )

    {% endset %}

    {% set results = run_query(sql) %}

    {% do log_query_results(
        results,
        'Delivery delay validation metrics'
    ) %}

{% endmacro %}
