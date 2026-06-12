"""API routes module.

Exports all route routers for the BI NBCR API. Each router handles a
smart-layer table; ``dbt_router`` exposes dbt execution.
"""

from app.routes.funil_imei import router as funil_imei_router
from app.routes.retorno_abr import router as retorno_abr_router
from app.routes.integracao_bncr import router as integracao_bncr_router
from app.routes.cadastro import router as cadastro_router
from app.routes.dbt import router as dbt_router

__all__ = [
    "funil_imei_router",
    "retorno_abr_router",
    "integracao_bncr_router",
    "cadastro_router",
    "dbt_router",
]
