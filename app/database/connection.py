"""Database connection and session management for BI NBCR API.

Suporta dois modos:

* **Databricks Apps** (produção): quando as variáveis ``PGHOST``/``PGUSER``/
  ``PGDATABASE`` são injetadas pelo recurso ``postgres`` do ``app.yaml``, a
  senha é um token OAuth obtido no endpoint OIDC do Databricks.
* **Local** (desenvolvimento): usa ``DATABASE_URL`` se definida; caso
  contrário, compõe a URL a partir das variáveis ``POSTGRES_*`` do ``.env``.
"""

import os
import time

import requests
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker

# Schema padrão consultado pela API (camada de consumo do dbt).
SEARCH_PATH = "smart"

_host = os.getenv("PGHOST")
_port = os.getenv("PGPORT", "5432")
_user = os.getenv("PGUSER")
_db = os.getenv("PGDATABASE")

if _host and _user and _db:
    # --- Databricks Apps: autenticação via token OAuth (OIDC) ---
    DATABASE_URL = f"postgresql+psycopg2://{_user}:@{_host}:{_port}/{_db}"
    engine = create_engine(DATABASE_URL, pool_pre_ping=True)

    _token = None
    _last_refresh = 0

    def _get_oauth_token():
        """Get OAuth token from Databricks OIDC endpoint."""
        db_host = os.environ["DATABRICKS_HOST"]
        client_id = os.environ["DATABRICKS_CLIENT_ID"]
        client_secret = os.environ["DATABRICKS_CLIENT_SECRET"]

        resp = requests.post(
            f"https://{db_host}/oidc/v1/token",
            data={
                "grant_type": "client_credentials",
                "client_id": client_id,
                "client_secret": client_secret,
                "scope": "all-apis",
            },
        )
        resp.raise_for_status()
        return resp.json()["access_token"]

    @event.listens_for(engine, "do_connect")
    def provide_token(dialect, conn_rec, cargs, cparams):
        global _token, _last_refresh
        if _token is None or time.time() - _last_refresh > 900:
            _token = _get_oauth_token()
            _last_refresh = time.time()
        cparams["password"] = _token
        cparams["sslmode"] = "require"
        cparams["options"] = f"-c search_path={SEARCH_PATH}"

else:
    # --- Local: DATABASE_URL ou variáveis POSTGRES_* do .env ---
    from dotenv import load_dotenv

    load_dotenv()

    DATABASE_URL = os.getenv("DATABASE_URL")
    if not DATABASE_URL:
        pg_user = os.getenv("POSTGRES_USER", "sinesp")
        pg_pass = os.getenv("POSTGRES_PASSWORD", "")
        pg_host = os.getenv("POSTGRES_HOST", "localhost")
        pg_port = os.getenv("POSTGRES_PORT", "5432")
        pg_db = os.getenv("POSTGRES_DB", "sinesp_ppe")
        DATABASE_URL = (
            f"postgresql+psycopg2://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_db}"
        )

    engine = create_engine(DATABASE_URL, pool_pre_ping=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """Yield a database session, closing it afterwards."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
