-- Padroniza os timestamps do Sinesp PPe para `timestamp`.
-- Trata dois formatos vindos do JSONB:
--   DT_*: '2026-06-11T15:56:25.262_America/Fortaleza'  (ISO com sufixo de timezone)
--   TS_*: '2026-06-11 12:56:24.857873'                 (sem sufixo)
-- O split_part remove o sufixo '_America/Fortaleza' quando existe; quando não
-- existe (TS_*), retorna a string inteira.
{% macro clean_ts(value) -%}
    nullif(split_part({{ value }}, '_', 1), '')::timestamp
{%- endmacro %}
