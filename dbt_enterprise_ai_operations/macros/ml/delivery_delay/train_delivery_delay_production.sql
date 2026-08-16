{% macro train_delivery_delay_production() %}

    {% set model_name =
        delivery_delay_model_name('delivery_delay_logistic')
    %}

    {% set feature_mart =
        ref('mart_delivery_features')
    %}

    {% set sql %}

        create or replace model {{ model_name }}

        options(
            model_type = 'LOGISTIC_REG',
            input_label_cols = ['target_is_delayed'],
            auto_class_weights = true,
            data_split_method = 'NO_SPLIT'
        )

        as

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

    {% endset %}

    {% do run_query(sql) %}

    {% do log(
        'Created production model: ' ~ model_name,
        info=true
    ) %}

{% endmacro %}
