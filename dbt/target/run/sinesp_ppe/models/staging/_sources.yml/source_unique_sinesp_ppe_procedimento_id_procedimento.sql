
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    

select
    id_procedimento as unique_field,
    count(*) as n_records

from "sinesp_ppe"."public"."procedimento"
where id_procedimento is not null
group by id_procedimento
having count(*) > 1



  
  
      
    ) dbt_internal_test