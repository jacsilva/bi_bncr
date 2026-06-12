-- Camada SMART: agrega o retorno ABR por operadora/grupo e data.

with retorno as (

    select * from "sinesp_ppe"."intermediate"."int_retorno_abr"

)

select
    operadora,
    operadora_grupo,
    data_referencia,
    sum(imeis_consultados)        as imeis_consultados,
    sum(imeis_ativos)             as imeis_ativos,
    sum(bloqueios_solicitados)    as bloqueios_solicitados,
    sum(bloqueios_efetivados)     as bloqueios_efetivados,
    avg(prazo_medio_dias)         as prazo_medio_dias,
    case when sum(bloqueios_solicitados) > 0
         then round(sum(bloqueios_efetivados)::numeric / sum(bloqueios_solicitados), 4)
    end                           as taxa_efetivacao
from retorno
group by operadora, operadora_grupo, data_referencia
order by operadora, data_referencia