-- Camada INTERMEDIATE: funil de IMEI enriquecido com a dimensão de UF.
-- Calcula as colunas-fórmula (não armazenadas no seed):
--   disponivel_recuperacao = roubados_furtados - bloqueados_operadora
--   taxa_qualidade         = imei_valido / total_celulares
--   taxa_disponibilidade   = disponivel_recuperacao / total_celulares
-- Obs.: linhas com uf = 'BR' são o total nacional (sem match em dim_uf).

with funil as (

    select * from "sinesp_ppe"."staging"."fato_funil_imei"

)

select
    f.data_referencia,
    f.uf,
    u.nome              as uf_nome,
    u.regiao,
    u.meio_envio,
    f.fonte,
    f.total_bo,
    f.total_celulares,
    f.imei_invalido,
    f.imei_valido,
    f.recuperados,
    f.roubados_furtados,
    f.encontrados_api_cellseg,
    f.recuperados_api,
    f.roufur_api,
    f.bloqueados_operadora,

    -- colunas calculadas (regra de negócio)
    (f.roubados_furtados - f.bloqueados_operadora)                          as disponivel_recuperacao,
    case when f.total_celulares > 0
         then round(f.imei_valido::numeric / f.total_celulares, 4)
    end                                                                     as taxa_qualidade,
    case when f.total_celulares > 0
         then round((f.roubados_furtados - f.bloqueados_operadora)::numeric / f.total_celulares, 4)
    end                                                                     as taxa_disponibilidade
from funil f
left join "sinesp_ppe"."staging"."dim_uf" u
    on f.uf = u.uf