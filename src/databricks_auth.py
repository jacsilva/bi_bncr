"""Autenticação no Databricks (Lakebase): token OAuth via OIDC.

No Databricks Apps, o resource injeta ``DATABRICKS_HOST``/``DATABRICKS_CLIENT_ID``/
``DATABRICKS_CLIENT_SECRET`` (service principal do app). O token resultante
(~1h de validade) é usado como senha do Postgres do Lakebase.

Centraliza a obtenção do token, evitando duplicação entre a API
(``app/database/connection.py``) e o pipeline dbt (``src/transform.py``).
"""

import os

import requests


def get_oauth_token() -> str:
    """Obtém um token OAuth no endpoint OIDC do Databricks (client_credentials)."""
    db_host = os.environ["DATABRICKS_HOST"]
    resp = requests.post(
        f"https://{db_host}/oidc/v1/token",
        data={
            "grant_type": "client_credentials",
            "client_id": os.environ["DATABRICKS_CLIENT_ID"],
            "client_secret": os.environ["DATABRICKS_CLIENT_SECRET"],
            "scope": "all-apis",
        },
    )
    resp.raise_for_status()
    return resp.json()["access_token"]
