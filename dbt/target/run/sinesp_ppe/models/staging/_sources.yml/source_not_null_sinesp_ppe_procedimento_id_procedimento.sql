
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select id_procedimento
from "sinesp_ppe"."public"."procedimento"
where id_procedimento is null



  
  
      
    ) dbt_internal_test