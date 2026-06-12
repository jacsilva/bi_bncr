-- Camada STAGING: limpeza e padronização dos campos vindos do JSONB.
-- Responsabilidades: tipagem, trim de texto, normalização de flags e
-- padronização de datas/timestamps. Primeiro estágio: usa source().

with origem as (

    select
        id_procedimento,
        dados,
        importado_em
    from "sinesp_ppe"."public"."procedimento"

)

select
    -- identificadores
    id_procedimento,
    (dados ->> 'NR_REGISTRO')::bigint                            as nr_registro,
    (dados ->> 'AN_REGISTRO')::int                               as an_registro,
    nullif(trim(dados ->> 'ID_UN_DELEGACIA_REGISTRO'), '')       as id_un_delegacia_registro,
    nullif(trim(dados ->> 'ID_UN_DELEGACIA_AFETO'), '')          as id_un_delegacia_afeto,
    (dados ->> 'ID_DELEGADO')::bigint                            as id_delegado,
    nullif(dados ->> 'ID_PROCEDIMENTO_PAI', '')::bigint          as id_procedimento_pai,
    nullif(dados ->> 'ID_PROCEDIMENTO_ADITADO', '')::bigint      as id_procedimento_aditado,

    -- texto padronizado (trim / upper onde faz sentido)
    upper(nullif(trim(dados ->> 'SG_UF_REGISTRO'), ''))          as sg_uf_registro,
    nullif(trim(dados ->> 'IN_TIPO_PROCEDIMENTO'), '')           as in_tipo_procedimento,
    nullif(trim(dados ->> 'IN_SITUACAO_ATUAL'), '')              as in_situacao_atual,
    nullif(trim(dados ->> 'TP_FORCA_ORIGEM'), '')                as tp_forca_origem,
    (dados ->> 'NR_ADENDO')::int                                 as nr_adendo,

    -- flags normalizadas para boolean
    (dados ->> 'SN_SIGILOSO')::int = 1                           as is_sigiloso,
    (dados ->> 'SN_ADENDO')::int = 1                             as is_adendo,
    (dados ->> 'SN_ADITADO')::int = 1                            as is_aditado,
    upper(trim(dados ->> 'SN_SITUACAO_HOMOLOGADO')) = 'SIM'      as is_homologado,

    -- datas/timestamps padronizados
    nullif(split_part(dados ->> 'DT_REGISTRO', '_', 1), '')::timestamp                    as dt_registro,
    nullif(split_part(dados ->> 'DT_PRIMEIRO_REGISTRO', '_', 1), '')::timestamp           as dt_primeiro_registro,
    nullif(split_part(dados ->> 'TS_CRIACAO', '_', 1), '')::timestamp                     as ts_criacao,
    nullif(split_part(dados ->> 'TS_ATUALIZACAO', '_', 1), '')::timestamp                 as ts_atualizacao,

    -- derivações de calendário (úteis para joins/agregações posteriores)
    (nullif(split_part(dados ->> 'DT_REGISTRO', '_', 1), '')::timestamp)::date            as dia_registro,
    extract(month from nullif(split_part(dados ->> 'DT_REGISTRO', '_', 1), '')::timestamp)::int as mes_registro,

    importado_em
from origem