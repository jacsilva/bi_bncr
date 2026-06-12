from datetime import date
from typing import Optional

from pydantic import BaseModel


class FunilImeiPorRegiaoSchema(BaseModel):
    """Schema for smt_funil_imei_por_regiao response serialization."""

    regiao: Optional[str] = None
    data_referencia: Optional[date] = None
    fonte: Optional[str] = None
    qt_ufs: Optional[int] = None
    total_bo: Optional[float] = None
    total_celulares: Optional[float] = None
    imei_valido: Optional[float] = None
    roubados_furtados: Optional[float] = None
    bloqueados_operadora: Optional[float] = None
    disponivel_recuperacao: Optional[float] = None
    taxa_qualidade: Optional[float] = None
    taxa_disponibilidade: Optional[float] = None

    class Config:
        from_attributes = True
