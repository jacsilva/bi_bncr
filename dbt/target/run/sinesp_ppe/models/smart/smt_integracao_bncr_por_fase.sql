
  
    

  create  table "sinesp_ppe"."smart"."smt_integracao_bncr_por_fase__dbt_tmp"
  
  
    as
  
  (
    -- Camada SMART: agrega a integração BNCR por fase (quantas UFs e tempo na fase).

with integracao as (

    select * from "sinesp_ppe"."intermediate"."int_integracao_bncr"

)

select
    fase,
    count(*)                 as qt_ufs,
    round(avg(dias_na_fase), 1)  as media_dias_na_fase,
    min(dias_na_fase)        as min_dias_na_fase,
    max(dias_na_fase)        as max_dias_na_fase
from integracao
group by fase
order by media_dias_na_fase desc
  );
  