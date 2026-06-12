"""Execução dos modelos dbt (transformação medallion) após a carga no banco."""

import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
DBT_DIR = BASE_DIR / "dbt"

# Garante que as variáveis POSTGRES_* estejam em os.environ — o profiles.yml
# do dbt as lê via env_var().
load_dotenv(BASE_DIR / ".env")


def run_dbt(command="run", select=None, exclude=None):
    """Executa um comando dbt (default: run) apontando para o projeto local.

    Aceita seleção opcional de nós via ``select``/``exclude`` (str ou lista),
    repassada como ``--select``/``--exclude`` ao dbt.

    Usa a API programática dbtRunner, que roda no mesmo interpretador/venv.
    Levanta RuntimeError se o dbt falhar.
    """
    from dbt.cli.main import dbtRunner

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
