-- Camada INTERMEDIATE: cadastros enriquecidos com a dimensão de UF.

with cadastro as (

    select * from {{ ref('fato_cadastro') }}

)

select
    c.data,
    c.uf,
    u.nome             as uf_nome,
    u.regiao,
    c.cadastros_recebidos,
    c.dispositivos_vinculados
from cadastro c
left join {{ ref('dim_uf') }} u
    on c.uf = u.uf
