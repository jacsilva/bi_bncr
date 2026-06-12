"""Model for the smart cadastro aggregation table."""

from sqlalchemy import Column, Date, Numeric, String

from app.database.base import Base


class CadastroPorRegiao(Base):
    """Model for the smart.smt_cadastro_por_regiao table."""

    __tablename__ = "smt_cadastro_por_regiao"
    __table_args__ = {"schema": "smart"}

    regiao = Column(String, primary_key=True)
    data = Column(Date, primary_key=True)
    cadastros_recebidos = Column(Numeric)
    dispositivos_vinculados = Column(Numeric)
