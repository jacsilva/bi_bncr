# BI NBCR

BI sobre o ciclo de bloqueio e recuperação de celulares (IMEI) no âmbito do
NBCR. Reúne, por UF e operadora, indicadores de:

- **Funil de IMEI** — volume de BOs/celulares, qualidade dos IMEIs e
  disponibilidade para recuperação.
- **Retorno ABR** — consultas e bloqueios solicitados/efetivados pelas
  operadoras.
- **Integração BNCR** — em que fase de adesão cada UF se encontra e há quanto
  tempo.
- **Cadastro** — cadastros recebidos e dispositivos vinculados.

## Stack

- **Postgres** em container Docker (ver `docker-compose.yml`).
- **dbt** (`dbt-core` + `dbt-postgres`) para as transformações, organizado em
  arquitetura **medallion**.

## Arquitetura (medallion)

| Camada | Schema | Materialização | Responsabilidade |
| --- | --- | --- | --- |
| Landing | `staging` | seeds | Dados de referência vindos de planilhas (dimensões e fatos). |
| Intermediate | `intermediate` | view (`int_*`) | JOINs com as dimensões + colunas-fórmula. |
| Smart | `smart` | table (`smt_*`) | Agregações prontas para consumo. |

## Modelo de dados

### Dimensões (seeds)

- `dim_uf` — UFs: `uf`, `nome`, `regiao`, `meio_envio`, `obs`.
- `dim_operadora` — operadoras: `codigo`, `operadora`, `grupo`, `ativa`.

### Fatos (seeds) e modelos derivados

Cada fato é carregado como seed (somente colunas-base; as colunas-fórmula são
calculadas nas camadas) e flui por `int_*` (joins) → `smt_*` (agregações):

| Fato (seed) | Intermediate (`int_*`) | Smart (`smt_*`) |
| --- | --- | --- |
| `fato_funil_imei` | `int_funil_imei` | `smt_funil_imei_por_regiao` |
| `fato_retorno_abr` | `int_retorno_abr` | `smt_retorno_abr_por_operadora` |
| `fato_integracao_bncr` | `int_integracao_bncr` | `smt_integracao_bncr_por_fase` |
| `fato_cadastro` | `int_cadastro` | `smt_cadastro_por_regiao` |

As **colunas-fórmula** nunca são digitadas nos seeds; são calculadas nas
camadas, por exemplo:

- `disponivel_recuperacao` = `roubados_furtados − bloqueados_operadora`
- `taxa_qualidade` = `imei_valido / total_celulares`
- `taxa_disponibilidade` = `disponivel_recuperacao / total_celulares`
- `taxa_efetivacao` = `bloqueios_efetivados / bloqueios_solicitados`
- `dias_na_fase` = `HOJE() − data_entrada_fase`

## Convenções

- Prefixos: **`int_`** para joins (intermediate), **`smt_`** para agregações
  (smart).
- Seeds vivem no schema `staging`, com `column_types` explícitos em
  `dbt/dbt_project.yml`.
- Novas tabelas seguem o mesmo fluxo: seed → `int_` → `smt_`.

## Como executar (somente dbt)

Esta é a forma de rodar o BI a partir dos seeds, **sem** a pipeline de
ingestão.

1. Suba o Postgres:

   ```bash
   docker compose up -d
   ```

2. Configure o `.env` na raiz com as variáveis do banco:

   ```env
   PGHOST=localhost
   PGPORT=5432
   PGDATABASE=bi_nbcr
   PGUSER=bi_nbcr
   POSTGRES_PASSWORD=...
   ```

3. Instale as dependências e rode o dbt:

   ```bash
   pip install -r requirements.txt
   python main.py --dbt-only
   ```

   `--dbt-only` executa `dbt seed` (carrega dimensões e fatos) seguido de
   `dbt run` (constrói os modelos `int_*`/`smt_*`), sem qualquer ingestão
   externa.

   Alternativamente, direto pela CLI do dbt:

   ```bash
   cd dbt
   dbt seed --profiles-dir .
   dbt run --profiles-dir .
   ```

## Estrutura do projeto

```
.
├── dbt/
│   ├── models/
│   │   ├── intermediate/   # int_* (joins)
│   │   └── smart/          # smt_* (agregações)
│   ├── seeds/              # dim_* e fato_* (CSV)
│   ├── macros/
│   ├── dbt_project.yml
│   └── profiles.yml
├── src/
│   └── transform.py        # runner programático do dbt
├── docker-compose.yml      # Postgres
├── requirements.txt
└── main.py                 # ponto de entrada
```
