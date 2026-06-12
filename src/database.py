"""Persistência dos resultados das queries no Postgres."""

import os
from pathlib import Path

import psycopg2
from psycopg2.extras import Json, execute_values
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

PG_CONFIG = {
    "host": os.getenv("PGHOST", "localhost"),
    "port": os.getenv("PGPORT", "5432"),
    "dbname": os.getenv("PGDATABASE", "sinesp_ppe"),
    "user": os.getenv("PGUSER", "sinesp"),
    "password": os.getenv("POSTGRES_PASSWORD", ""),
}
TABLE = os.getenv("POSTGRES_TABLE", "procedimento")


def get_pg_connection():
    """Abre uma conexão com o Postgres."""
    return psycopg2.connect(**PG_CONFIG)


def _ensure_table(cursor):
    """Cria a tabela (se não existir). O registro completo fica em JSONB."""
    cursor.execute(
        f"""
        CREATE TABLE IF NOT EXISTS {TABLE} (
            id_procedimento BIGINT PRIMARY KEY,
            dados           JSONB NOT NULL,
            importado_em    TIMESTAMPTZ NOT NULL DEFAULT now()
        );
        """
    )


def save_results_to_db(results):
    """Grava as linhas retornadas pelas queries na tabela do Postgres.

    Cada linha é armazenada como JSONB, com upsert por id_procedimento.
    """
    rows = []
    for query_result in results:
        for row in query_result.get("data", []):
            pk = row.get("ID_PROCEDIMENTO")
            if pk is None:
                continue
            rows.append((pk, Json(row)))

    if not rows:
        print("\nNenhuma linha com ID_PROCEDIMENTO para gravar no banco.")
        return 0

    conn = get_pg_connection()
    try:
        with conn, conn.cursor() as cursor:
            _ensure_table(cursor)
            execute_values(
                cursor,
                f"""
                INSERT INTO {TABLE} (id_procedimento, dados)
                VALUES %s
                ON CONFLICT (id_procedimento) DO UPDATE
                    SET dados = EXCLUDED.dados,
                        importado_em = now();
                """,
                rows,
            )
    finally:
        conn.close()

    print(
        f"\nTotal: {len(rows)} linha(s) gravada(s) na tabela "
        f"'{TABLE}' do banco '{PG_CONFIG['dbname']}'."
    )
    return len(rows)
