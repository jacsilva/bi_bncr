from typing import Optional

from pydantic import BaseModel


class IntegracaoBncrPorFaseSchema(BaseModel):
    """Schema for smt_integracao_bncr_por_fase response serialization."""

    fase: Optional[str] = None
    qt_ufs: Optional[int] = None
    media_dias_na_fase: Optional[float] = None
    min_dias_na_fase: Optional[int] = None
    max_dias_na_fase: Optional[int] = None

    class Config:
        from_attributes = True
