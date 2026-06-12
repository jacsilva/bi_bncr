from datetime import date
from typing import Optional

from pydantic import BaseModel


class RetornoAbrPorOperadoraSchema(BaseModel):
    """Schema for smt_retorno_abr_por_operadora response serialization."""

    operadora: Optional[str] = None
    operadora_grupo: Optional[str] = None
    data_referencia: Optional[date] = None
    imeis_consultados: Optional[float] = None
    imeis_ativos: Optional[float] = None
    bloqueios_solicitados: Optional[float] = None
    bloqueios_efetivados: Optional[float] = None
    prazo_medio_dias: Optional[float] = None
    taxa_efetivacao: Optional[float] = None

    class Config:
        from_attributes = True
