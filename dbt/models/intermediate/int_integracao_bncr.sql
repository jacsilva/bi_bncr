-- Camada INTERMEDIATE: integração BNCR enriquecida com a dimensão de UF.
-- Calcula dias_na_fase = HOJE() - data_entrada_fase.

with integracao as (

    select * from {{ ref('fato_integracao_bncr') }}

)

select
    i.uf,
    u.nome             as uf_nome,
    u.regiao,
    i.fase,
    i.data_entrada_fase,
    i.processo_sei,
    i.ponto_focal,
    i.observacao,

    -- coluna calculada
    (current_date - i.data_entrada_fase)   as dias_na_fase
from integracao i
left join {{ ref('dim_uf') }} u
    on i.uf = u.uf
