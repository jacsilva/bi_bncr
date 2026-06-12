"""Integração BNCR (smart) API routes."""

from typing import List, Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.dependencies import verify_api_key
from app.models import IntegracaoBncrPorFase
from app.schemas import IntegracaoBncrPorFaseSchema

router = APIRouter(prefix="/integracao-bncr", tags=["integracao_bncr"])


@router.get(
    "",
    response_model=List[IntegracaoBncrPorFaseSchema],
    summary="Listar integração BNCR por fase",
    description="Retorna a integração BNCR agregada por fase, com filtro opcional.",
)
def list_integracao_bncr(
    fase: Optional[str] = Query(None, description="Filtrar por fase"),
    db: Session = Depends(get_db),
    x_api_key: str = Depends(verify_api_key),
) -> List[IntegracaoBncrPorFase]:
    """List aggregated integração BNCR records."""
    query = db.query(IntegracaoBncrPorFase)
    if fase:
        query = query.filter(IntegracaoBncrPorFase.fase == fase)
    return query.all()


@router.get(
    "/count",
    summary="Contar registros da integração BNCR",
    description="Retorna o total de registros agregados da integração BNCR.",
)
def count_integracao_bncr(
    db: Session = Depends(get_db),
    x_api_key: str = Depends(verify_api_key),
) -> dict:
    """Count aggregated integração BNCR records."""
    total = db.query(func.count()).select_from(IntegracaoBncrPorFase).scalar()
    return {"total": total or 0}
