-- Camada INTERMEDIATE: cadastros enriquecidos com a dimensão de UF.

with cadastro as (

    select * from "sinesp_ppe"."staging"."fato_cadastro"

)

select
    c.data,
    c.uf,
    u.nome             as uf_nome,
    u.regiao,
    c.cadastros_recebidos,
    c.dispositivos_vinculados
from cadastro c
left join "sinesp_ppe"."staging"."dim_uf" u
    on c.uf = u.uf