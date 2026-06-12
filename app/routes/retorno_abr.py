"""Retorno ABR (smart) API routes."""

from typing import List, Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.dependencies import verify_api_key
from app.models import RetornoAbrPorOperadora
from app.schemas import RetornoAbrPorOperadoraSchema

router = APIRouter(prefix="/retorno-abr", tags=["retorno_abr"])


@router.get(
    "",
    response_model=List[RetornoAbrPorOperadoraSchema],
    summary="Listar retorno ABR por operadora",
    description="Retorna o retorno ABR agregado por operadora/grupo, com filtros opcionais.",
)
def list_retorno_abr(
    operadora: Optional[str] = Query(None, description="Filtrar por operadora"),
    db: Session = Depends(get_db),
    x_api_key: str = Depends(verify_api_key),
) -> List[RetornoAbrPorOperadora]:
    """List aggregated retorno ABR records."""
    query = db.query(RetornoAbrPorOperadora)
    if operadora:
        query = query.filter(RetornoAbrPorOperadora.operadora == operadora)
    return query.all()


@router.get(
    "/count",
    summary="Contar registros do retorno ABR",
    description="Retorna o total de registros agregados do retorno ABR.",
)
def count_retorno_abr(
    db: Session = Depends(get_db),
    x_api_key: str = Depends(verify_api_key),
) -> dict:
    """Count aggregated retorno ABR records."""
    total = db.query(func.count()).select_from(RetornoAbrPorOperadora).scalar()
    return {"total": total or 0}
