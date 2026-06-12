"""Model for the smart integração BNCR aggregation table."""

from sqlalchemy import Column, Integer, Numeric, BigInteger, String

from app.database.base import Base


class IntegracaoBncrPorFase(Base):
    """Model for the smart.smt_integracao_bncr_por_fase table."""

    __tablename__ = "smt_integracao_bncr_por_fase"
    __table_args__ = {"schema": "smart"}

    fase = Column(String, primary_key=True)
    qt_ufs = Column(BigInteger)
    media_dias_na_fase = Column(Numeric)
    min_dias_na_fase = Column(Integer)
    max_dias_na_fase = Column(Integer)
