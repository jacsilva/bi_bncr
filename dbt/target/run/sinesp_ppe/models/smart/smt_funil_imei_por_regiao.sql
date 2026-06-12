
  
    

  create  table "sinesp_ppe"."smart"."smt_funil_imei_por_regiao__dbt_tmp"
  
  
    as
  
  (
    -- Camada SMART: agrega o funil de IMEI por região (exclui o total nacional BR
-- para não dupli­car contagens). Recalcula as taxas no nível agregado.

with funil as (

    select * from "sinesp_ppe"."intermediate"."int_funil_imei"
    where uf <> 'BR'

)

select
    regiao,
    data_referencia,
    fonte,
    count(distinct uf)                          as qt_ufs,
    sum(total_bo)                               as total_bo,
    sum(total_celulares)                        as total_celulares,
    sum(imei_valido)                            as imei_valido,
    sum(roubados_furtados)                      as roubados_furtados,
    sum(bloqueados_operadora)                   as bloqueados_operadora,
    sum(disponivel_recuperacao)                 as disponivel_recuperacao,
    case when sum(total_celulares) > 0
         then round(sum(imei_valido)::numeric / sum(total_celulares), 4)
    end                                         as taxa_qualidade,
    case when sum(total_celulares) > 0
         then round(sum(disponivel_recuperacao)::numeric / sum(total_celulares), 4)
    end                                         as taxa_disponibilidade
from funil
group by regiao, data_referencia, fonte
order by regiao, data_referencia, fonte
  );
  