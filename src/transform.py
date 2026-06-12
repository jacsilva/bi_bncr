"""Execução dos modelos dbt (transformação medallion) após a carga no banco."""

import os
import uuid
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
DBT_DIR = BASE_DIR / "dbt"

# Garante que as variáveis POSTGRES_*/PG* estejam em os.environ — o profiles.yml
# do dbt as lê via env_var().
load_dotenv(BASE_DIR / ".env")


def _ensure_pgpassword():
    """Garante que ``PGPASSWORD`` esteja definido antes de invocar o dbt.

    No Databricks Apps (Lakebase) a senha é um token OAuth de curta duração
    (~1h) gerado em runtime via SDK; PGHOST/PGPORT/PGUSER/PGDATABASE são
    injetados pelo resource ``postgres``. Localmente, usa a senha estática do
    Postgres em container (``POSTGRES_PASSWORD`` no .env).
    """
    # Ambiente Databricks Apps: o resource injeta as credenciais do service
    # principal (DATABRICKS_CLIENT_ID). Gera o token OAuth a cada execução.
    if os.environ.get("DATABRICKS_CLIENT_ID"):
        from databricks.sdk import WorkspaceClient

        w = WorkspaceClient()
        # ✅ Usar PGDATABASE injetado pelo Lakebase (databricks-postgres com hífen)
        cred = w.database.generate_database_credential(
            request_id=str(uuid.uuid4()),
            instance_names=[os.environ.get("PGDATABASE", "databricks-postgres")]
        )
        os.environ["PGPASSWORD"] = cred.token
        return

    # Ambiente local: usa a senha estática do Postgres do .env, se PGPASSWORD
    # ainda não estiver definido.
    if not os.environ.get("PGPASSWORD") and os.environ.get("POSTGRES_PASSWORD"):
        os.environ["PGPASSWORD"] = os.environ["POSTGRES_PASSWORD"]


def run_dbt(command="run", select=None, exclude=None):
    """Executa um comando dbt (default: run) apontando para o projeto local.

    Aceita seleção opcional de nós via ``select``/``exclude`` (str ou lista),
    repassada como ``--select``/``--exclude`` ao dbt.

    Usa a API programática dbtRunner, que roda no mesmo interpretador/venv.
    Levanta RuntimeError se o dbt falhar.
    """
    from dbt.cli.main import dbtRunner

    _ensure_pgpassword()

    cli_args = [
        command,
        "--project-dir", str(DBT_DIR),
        "--profiles-dir", str(DBT_DIR),
    ]

    if select:
        cli_args += ["--select", *(select if isinstance(select, list) else [select])]
    if exclude:
        cli_args += ["--exclude", *(exclude if isinstance(exclude, list) else [exclude])]

    print(f"\nExecutando dbt ({command}) sobre os dados carregados...")
    result = dbtRunner().invoke(cli_args)

    if not result.success:
        raise RuntimeError(f"Execução do dbt falhou: {result.exception}")

    return result
