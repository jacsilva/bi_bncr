"""dbt execution API routes.

Disponibiliza a execução das transformações dbt (medallion) via API,
reaproveitando ``src.transform.run_dbt``. Os endpoints são protegidos por
API key e rodam de forma síncrona (FastAPI os executa em threadpool).
"""

import sys
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException

from app.dependencies import verify_api_key
from app.schemas import DbtResponse, DbtRunRequest

# Garante que o pacote ``src`` (raiz do projeto) seja importável.
_PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from src.transform import run_dbt  # noqa: E402

# Exclui a linhagem de procedimento (acoplada à pipeline de ingestão).
DBT_EXCLUDE = "stg_procedimento+"

router = APIRouter(prefix="/dbt", tags=["dbt"])


def _invoke(command: str, select=None, exclude=None) -> DbtResponse:
    """Run a dbt command and translate the outcome into a DbtResponse."""
    try:
        run_dbt(command, select=select, exclude=exclude)
    except RuntimeError as exc:
        raise HTTPException(status_code=500, detail=str(exc))
    return DbtResponse(
        success=True,
        command=command,
        message=f"dbt {command} executado com sucesso.",
    )


@router.post(
    "/seed",
    response_model=DbtResponse,
    summary="Carregar seeds (dbt seed)",
    description="Carrega/atualiza as seeds (dimensões e fatos) no banco.",
)
def dbt_seed(x_api_key: str = Depends(verify_api_key)) -> DbtResponse:
    """Run `dbt seed`."""
    return _invoke("seed")


@router.post(
    "/run",
    response_model=DbtResponse,
    summary="Executar modelos (dbt run)",
    description=(
        "Constrói os modelos do BI (intermediate/smart), excluindo a linhagem "
        "de procedimento. Aceita seleção opcional via 'select'/'exclude'."
    ),
)
def dbt_run(
    body: DbtRunRequest | None = None,
    x_api_key: str = Depends(verify_api_key),
) -> DbtResponse:
    """Run `dbt run`, excluding procedimento by default."""
    select = body.select if body else None
    exclude = body.exclude if body and body.exclude else [DBT_EXCLUDE]
    return _invoke("run", select=select, exclude=exclude)


@router.post(
    "/build",
    response_model=DbtResponse,
    summary="Seed + run (BI completo)",
    description="Roda 'dbt seed' seguido de 'dbt run' (sem procedimento).",
)
def dbt_build(x_api_key: str = Depends(verify_api_key)) -> DbtResponse:
    """Run `dbt seed` then `dbt run` (BI pipeline, sem procedimento)."""
    _invoke("seed")
    return _invoke("run", exclude=[DBT_EXCLUDE])
