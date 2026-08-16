{% macro delivery_delay_model_name(model_name) %}
    {% set dataset_name = target.schema ~ '_ml' %}
    {{ return('`' ~ target.database ~ '.' ~ dataset_name ~ '.' ~ model_name ~ '`') }}
{% endmacro %}
