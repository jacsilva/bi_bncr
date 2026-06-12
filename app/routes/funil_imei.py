"""Funil de IMEI (smart) API routes."""

from typing import List, Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.dependencies import verify_api_key
from app.models import FunilImeiPorRegiao
from app.schemas import FunilImeiPorRegiaoSchema

router = APIRouter(prefix="/funil-imei", tags=["funil_imei"])


@router.get(
    "",
    response_model=List[FunilImeiPorRegiaoSchema],
    summary="Listar funil de IMEI por região",
    description="Retorna o funil de IMEI agregado por região, com filtros opcionais.",
)
def list_funil_imei(
    regiao: Optional[str] = Query(None, description="Filtrar por região"),
    fonte: Optional[str] = Query(None, description="Filtrar por fonte"),
    db: Session = Depends(get_db),
    x_api_key: str = Depends(verify_api_key),
) -> List[FunilImeiPorRegiao]:
    """List aggregated funil de IMEI records."""
    query = db.query(FunilImeiPorRegiao)
    if regiao:
        query = query.filter(FunilImeiPorRegiao.regiao == regiao)
    if fonte:
        query = query.filter(FunilImeiPorRegiao.fonte == fonte)
    return query.all()


@router.get(
    "/count",
    summary="Contar registros do funil de IMEI",
    description="Retorna o total de registros agregados do funil de IMEI.",
)
def count_funil_imei(
    db: Session = Depends(get_db),
    x_api_key: str = Depends(verify_api_key),
) -> dict:
    """Count aggregated funil de IMEI records."""
    total = db.query(func.count()).select_from(FunilImeiPorRegiao).scalar()
    return {"total": total or 0}
