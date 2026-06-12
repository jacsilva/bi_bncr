"""BI NBCR API - FastAPI application.

Expõe os dados da camada smart (consumo do BI) e a execução das
transformações dbt. Inclui endpoints de health check e configuração de CORS.
"""

import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from app.database.connection import SessionLocal
from app.routes import (
    funil_imei_router,
    retorno_abr_router,
    integracao_bncr_router,
    cadastro_router,
    dbt_router,
)

app = FastAPI(
    title="BI NBCR API",
    description="API para acesso aos dados smart do BI NBCR e execução do dbt.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

_frontend_url = os.getenv("FRONTEND_URL", "http://localhost:8081")
_allowed_origins = [_frontend_url]

app.add_middleware(
    CORSMiddleware,
    allow_origins=_allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(funil_imei_router, prefix="/api")
app.include_router(retorno_abr_router, prefix="/api")
app.include_router(integracao_bncr_router, prefix="/api")
app.include_router(cadastro_router, prefix="/api")
app.include_router(dbt_router, prefix="/api")


@app.get(
    "/",
    summary="Raiz da API",
    description="Retorna informações básicas sobre a API.",
)
def root() -> dict:
    """Return basic API information."""
    return {"message": "BI NBCR API está rodando", "version": "1.0.0"}


@app.get(
    "/health",
    summary="Verificação de saúde",
    description="Verifica a saúde da API e a conexão com o banco de dados.",
    tags=["health"],
)
def health_check() -> dict:
    """Check API and database health."""
    db = SessionLocal()
    try:
        db.execute(text("SELECT 1"))
        return {"status": "healthy", "database": "connected"}
    except Exception:
        return {"status": "unhealthy", "database": "disconnected"}
    finally:
        db.close()
