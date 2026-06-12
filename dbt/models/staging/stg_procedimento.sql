-- Camada STAGING: limpeza e padronização dos campos vindos do JSONB.
-- Responsabilidades: tipagem, trim de texto, normalização de flags e
-- padronização de datas/timestamps. Primeiro estágio: usa source().

with origem as (

    select
        id_procedimento,
        dados,
        importado_em
    from {{ source('bi_bncr', 'procedimento') }}

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
    {{ clean_ts("dados ->> 'DT_REGISTRO'") }}                    as dt_registro,
    {{ clean_ts("dados ->> 'DT_PRIMEIRO_REGISTRO'") }}           as dt_primeiro_registro,
    {{ clean_ts("dados ->> 'TS_CRIACAO'") }}                     as ts_criacao,
    {{ clean_ts("dados ->> 'TS_ATUALIZACAO'") }}                 as ts_atualizacao,

    -- derivações de calendário (úteis para joins/agregações posteriores)
    ({{ clean_ts("dados ->> 'DT_REGISTRO'") }})::date            as dia_registro,
    extract(month from {{ clean_ts("dados ->> 'DT_REGISTRO'") }})::int as mes_registro,

    importado_em
from origem
