
    
    

select
    id_procedimento as unique_field,
    count(*) as n_records

from "sinesp_ppe"."public"."procedimento"
where id_procedimento is not null
group by id_procedimento
having count(*) > 1


