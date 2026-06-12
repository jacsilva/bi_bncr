-- Camada SMART: agrega os cadastros por região e data.

with cadastro as (

    select * from "sinesp_ppe"."intermediate"."int_cadastro"

)

select
    regiao,
    data,
    sum(cadastros_recebidos)      as cadastros_recebidos,
    sum(dispositivos_vinculados)  as dispositivos_vinculados
from cadastro
group by regiao, data
order by regiao, data