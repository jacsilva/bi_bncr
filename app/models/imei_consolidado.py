"""Model for the silver IMEI consolidado table."""

from sqlalchemy import Boolean, Column, Date, DateTime, Integer, String

from app.database.base import Base


class ImeiConsolidado(Base):
    """Model for the silver.imei_consolidado table."""

    __tablename__ = "imei_consolidado"
    __table_args__ = {"schema": "silver"}

    imei = Column(String, primary_key=True)
    ultimo_status = Column(String)
    origem_status = Column(String)
    data_status = Column(Date)
    is_restricted = Column(Boolean)
    em_abrtelecom = Column(Boolean)
    em_bnbo = Column(Boolean)
    em_operadoras = Column(Boolean)
    em_estados = Column(Boolean)
    qtd_fontes = Column(Integer)
    data_consolidacao = Column(DateTime)
