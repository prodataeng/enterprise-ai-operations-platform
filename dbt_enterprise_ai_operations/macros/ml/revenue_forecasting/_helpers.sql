{% macro revenue_ml_dataset() %}
    {{ return(target.schema ~ '_ml') }}
{% endmacro %}

{% macro revenue_ml_model_name(model_name) %}
    {{ return('`' ~ target.project ~ '.' ~ revenue_ml_dataset() ~ '.' ~ model_name ~ '`') }}
{% endmacro %}

{% macro log_query_results(results, title='Query results') %}
    {% if execute and results is not none %}
        {% do log('', info=true) %}
        {% do log('=== ' ~ title ~ ' ===', info=true) %}
        {% do log(results.column_names | join(' | '), info=true) %}
        {% for row in results.rows %}
            {% set values = [] %}
            {% for value in row %}
                {% do values.append(value | string) %}
            {% endfor %}
            {% do log(values | join(' | '), info=true) %}
        {% endfor %}
        {% do log('=== end ===', info=true) %}
    {% endif %}
{% endmacro %}
