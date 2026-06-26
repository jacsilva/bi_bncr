"""IMEI consolidado (silver) API routes."""

from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.dependencies import verify_api_key
from app.models import ImeiConsolidado
from app.schemas import ImeiConsolidadoSchema

router = APIRouter(prefix="/imei-consolidado", tags=["imei_consolidado"])


@router.get(
    "/{imei}",
    response_model=ImeiConsolidadoSchema,
    summary="Consultar IMEI consolidado",
    description="Retorna os dados consolidados de um IMEI específico.",
)
def get_imei_consolidado(
    imei: str = Path(..., description="IMEI a ser consultado"),
    db: Session = Depends(get_db),
    x_api_key: str = Depends(verify_api_key),
) -> ImeiConsolidado:
    """Return the consolidated record for a single IMEI."""
    registro = db.get(ImeiConsolidado, imei)
    if registro is None:
        raise HTTPException(
            status_code=404,
            detail=f"IMEI '{imei}' não encontrado.",
        )
    return registro
