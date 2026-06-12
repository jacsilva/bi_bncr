"""Model for the smart retorno ABR aggregation table."""

from sqlalchemy import Column, Date, Numeric, String

from app.database.base import Base


class RetornoAbrPorOperadora(Base):
    """Model for the smart.smt_retorno_abr_por_operadora table."""

    __tablename__ = "smt_retorno_abr_por_operadora"
    __table_args__ = {"schema": "smart"}

    operadora = Column(String, primary_key=True)
    operadora_grupo = Column(String)
    data_referencia = Column(Date, primary_key=True)
    imeis_consultados = Column(Numeric)
    imeis_ativos = Column(Numeric)
    bloqueios_solicitados = Column(Numeric)
    bloqueios_efetivados = Column(Numeric)
    prazo_medio_dias = Column(Numeric)
    taxa_efetivacao = Column(Numeric)
