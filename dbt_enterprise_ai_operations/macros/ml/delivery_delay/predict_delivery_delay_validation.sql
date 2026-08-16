{% macro predict_delivery_delay_validation(
    test_start_date='2026-06-01',
    test_end_date='2026-07-31',
    threshold=0.5,
    limit_rows=50
) %}

    {% set model_name =
        delivery_delay_model_name('delivery_delay_logistic_validation')
    %}

    {% set feature_mart =
        ref('mart_delivery_features')
    %}

    {% set sql %}

        with predictions as (

            select *
            from ml.predict(
                model {{ model_name }},

                (
                    select
                        shipment_id,
                        order_id,
                        date_key,
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

        )

        select
            shipment_id,
            order_id,
            date_key,
            country_code,
            carrier,
            target_is_delayed as actual_is_delayed,
            predicted_target_is_delayed as predicted_is_delayed,

            (
                select prob
                from unnest(predicted_target_is_delayed_probs)
                where label = true
            ) as delay_probability

        from predictions

        order by
            delay_probability desc,
            date_key desc

        limit {{ limit_rows }}

    {% endset %}

    {% set results = run_query(sql) %}

    {% do log_query_results(
        results,
        'Delivery delay validation predictions'
    ) %}

{% endmacro %}
