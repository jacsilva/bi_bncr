"""Cadastro (smart) API routes."""

from typing import List, Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.dependencies import verify_api_key
from app.models import CadastroPorRegiao
from app.schemas import CadastroPorRegiaoSchema

router = APIRouter(prefix="/cadastro", tags=["cadastro"])


@router.get(
    "",
    response_model=List[CadastroPorRegiaoSchema],
    summary="Listar cadastros por região",
    description="Retorna os cadastros agregados por região, com filtro opcional.",
)
def list_cadastro(
    regiao: Optional[str] = Query(None, description="Filtrar por região"),
    db: Session = Depends(get_db),
    x_api_key: str = Depends(verify_api_key),
) -> List[CadastroPorRegiao]:
    """List aggregated cadastro records."""
    query = db.query(CadastroPorRegiao)
    if regiao:
        query = query.filter(CadastroPorRegiao.regiao == regiao)
    return query.all()


@router.get(
    "/count",
    summary="Contar registros de cadastro",
    description="Retorna o total de registros agregados de cadastro.",
)
def count_cadastro(
    db: Session = Depends(get_db),
    x_api_key: str = Depends(verify_api_key),
) -> dict:
    """Count aggregated cadastro records."""
    total = db.query(func.count()).select_from(CadastroPorRegiao).scalar()
    return {"total": total or 0}
