-- Camada INTERMEDIATE: joins. Enriquece cada procedimento com os dados do
-- seu procedimento pai (self-join). Usa ref() sobre o staging.

with proc as (

    select * from {{ ref('stg_procedimento') }}

)

select
    -- procedimento
    p.id_procedimento,
    p.nr_registro,
    p.an_registro,
    p.sg_uf_registro,
    p.in_tipo_procedimento,
    p.in_situacao_atual,
    p.tp_forca_origem,
    p.id_delegado,
    p.id_un_delegacia_registro,
    p.id_un_delegacia_afeto,
    p.is_sigiloso,
    p.is_adendo,
    p.is_aditado,
    p.is_homologado,
    p.dt_registro,
    p.dia_registro,
    p.mes_registro,

    -- procedimento pai (via join)
    p.id_procedimento_pai,
    pai.nr_registro          as pai_nr_registro,
    pai.in_tipo_procedimento as pai_in_tipo_procedimento,
    pai.dt_registro          as pai_dt_registro,
    (p.id_procedimento_pai is not null and pai.id_procedimento is not null) as tem_pai,

    p.importado_em
from proc p
left join proc pai
    on p.id_procedimento_pai = pai.id_procedimento
