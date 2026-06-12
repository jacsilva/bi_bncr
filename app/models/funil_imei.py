"""Model for the smart funil de IMEI aggregation table."""

from sqlalchemy import Column, Date, Numeric, BigInteger, String

from app.database.base import Base


class FunilImeiPorRegiao(Base):
    """Model for the smart.smt_funil_imei_por_regiao table."""

    __tablename__ = "smt_funil_imei_por_regiao"
    __table_args__ = {"schema": "smart"}

    regiao = Column(String, primary_key=True)
    data_referencia = Column(Date, primary_key=True)
    fonte = Column(String, primary_key=True)
    qt_ufs = Column(BigInteger)
    total_bo = Column(Numeric)
    total_celulares = Column(Numeric)
    imei_valido = Column(Numeric)
    roubados_furtados = Column(Numeric)
    bloqueados_operadora = Column(Numeric)
    disponivel_recuperacao = Column(Numeric)
    taxa_qualidade = Column(Numeric)
    taxa_disponibilidade = Column(Numeric)
