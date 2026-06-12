-- Camada INTERMEDIATE: retorno ABR enriquecido com operadora e UF.
-- Calcula taxa_efetivacao = bloqueios_efetivados / bloqueios_solicitados.

with retorno as (

    select * from {{ ref('fato_retorno_abr') }}

)

select
    r.data_referencia,
    r.operadora,
    o.operadora        as operadora_nome,
    o.grupo            as operadora_grupo,
    r.uf,
    u.nome             as uf_nome,
    u.regiao,
    r.imeis_consultados,
    r.imeis_ativos,
    r.bloqueios_solicitados,
    r.bloqueios_efetivados,
    r.prazo_medio_dias,

    -- coluna calculada
    case when r.bloqueios_solicitados > 0
         then round(r.bloqueios_efetivados::numeric / r.bloqueios_solicitados, 4)
    end                as taxa_efetivacao
from retorno r
left join {{ ref('dim_operadora') }} o
    on r.operadora = o.codigo
left join {{ ref('dim_uf') }} u
    on r.uf = u.uf
