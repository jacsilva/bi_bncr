-- Usa o schema custom (+schema do dbt_project.yml) exatamente como definido,
-- sem o prefixo do target. Assim cada camada vai para seu próprio schema:
-- staging / intermediate / smart.
{% macro generate_schema_name(custom_schema_name, node) -%}

    {%- set default_schema = target.schema -%}
    {%- if custom_schema_name is none -%}
        {{ default_schema }}
    {%- else -%}
        {{ custom_schema_name | trim }}
    {%- endif -%}

{%- endmacro %}
