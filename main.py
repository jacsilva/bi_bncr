"""Ponto de entrada: conecta ao Sinesp PPe, executa o SQL e salva o resultado.

Uso:
    python main.py              # pipeline completa (ingestão + dbt run)
    python main.py --dbt-only   # apenas dbt (seed + run), sem a ingestão
"""

import sys
from pathlib import Path

from src.transform import run_dbt

BASE_DIR = Path(__file__).resolve().parent
SQL_FILE = BASE_DIR / "sql" / "procedimentos.sql"

# Exclui a linhagem de procedimento quando rodamos só o dbt (BI por seeds).
DBT_ONLY_EXCLUDE = "stg_procedimento+"


def run_dbt_only():
    """Executa apenas o dbt (seeds + modelos), sem a pipeline de ingestão.

    Carrega as seeds (dimensões e fatos) e constrói os modelos do BI,
    excluindo a linhagem de procedimento (que depende da pipeline).
    """
    run_dbt("seed")
    run_dbt("run", exclude=DBT_ONLY_EXCLUDE)


def main():
    # Imports da pipeline ficam locais para que `--dbt-only` não exija
    # Java/JDBC nem as dependências de ingestão.
    from src.connect_ppe import get_connection
    from src.procedimento import run_queries
    from src.database import save_results_to_db

    conn = get_connection()
    try:
        sql_content = SQL_FILE.read_text(encoding="utf-8")
        print(f"\nLido arquivo SQL: {SQL_FILE}")

        results = run_queries(conn, sql_content)
        gravadas = save_results_to_db(results)
    finally:
        conn.close()

    # Após a carga no banco, executa as transformações dbt (medallion).
    if gravadas:
        run_dbt("run")
    else:
        print("\nSem linhas novas no banco; dbt não executado.")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] in ("--dbt-only", "dbt"):
        run_dbt_only()
    else:
        main()
