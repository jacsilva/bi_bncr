-- Camada SMART: agregações prontas para consumo (materializada como tabela).
-- Usa ref() sobre o intermediate.

with intermediario as (

    select * from {{ ref('int_procedimento') }}

)

select
    sg_uf_registro,
    an_registro,
    mes_registro,
    count(*)                                as qt_procedimentos,
    count(*) filter (where is_sigiloso)     as qt_sigilosos,
    count(*) filter (where is_aditado)      as qt_aditados,
    count(*) filter (where is_homologado)   as qt_homologados,
    count(*) filter (where tem_pai)         as qt_com_pai,
    count(distinct in_tipo_procedimento)    as qt_tipos_distintos,
    max(dt_registro)                        as ultimo_registro
from intermediario
group by sg_uf_registro, an_registro, mes_registro
order by sg_uf_registro, an_registro, mes_registro
