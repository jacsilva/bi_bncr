"""SQLAlchemy models for BI NBCR API.

Exports the smart-layer aggregation models consumed by the API.

Models:
    FunilImeiPorRegiao: Funil de IMEI agregado por região.
    RetornoAbrPorOperadora: Retorno ABR agregado por operadora/grupo.
    IntegracaoBncrPorFase: Integração BNCR agregada por fase.
    CadastroPorRegiao: Cadastros agregados por região.
    ImeiConsolidado: Dados consolidados por IMEI.
"""

from app.models.funil_imei import FunilImeiPorRegiao
from app.models.retorno_abr import RetornoAbrPorOperadora
from app.models.integracao_bncr import IntegracaoBncrPorFase
from app.models.cadastro import CadastroPorRegiao
from app.models.imei_consolidado import ImeiConsolidado

__all__ = [
    "FunilImeiPorRegiao",
    "RetornoAbrPorOperadora",
    "IntegracaoBncrPorFase",
    "CadastroPorRegiao",
    "ImeiConsolidado",
]
