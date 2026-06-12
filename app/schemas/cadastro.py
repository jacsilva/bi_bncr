from datetime import date
from typing import Optional

from pydantic import BaseModel


class CadastroPorRegiaoSchema(BaseModel):
    """Schema for smt_cadastro_por_regiao response serialization."""

    regiao: Optional[str] = None
    data: Optional[date] = None
    cadastros_recebidos: Optional[float] = None
    dispositivos_vinculados: Optional[float] = None

    class Config:
        from_attributes = True
