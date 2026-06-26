from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel


class ImeiConsolidadoSchema(BaseModel):
    """Schema for silver.imei_consolidado response serialization."""

    imei: Optional[str] = None
    ultimo_status: Optional[str] = None
    origem_status: Optional[str] = None
    data_status: Optional[date] = None
    is_restricted: Optional[bool] = None
    em_abrtelecom: Optional[bool] = None
    em_bnbo: Optional[bool] = None
    em_operadoras: Optional[bool] = None
    em_estados: Optional[bool] = None
    qtd_fontes: Optional[int] = None
    data_consolidacao: Optional[datetime] = None

    class Config:
        from_attributes = True
