from typing import List, Optional

from pydantic import BaseModel


class DbtRunRequest(BaseModel):
    """Request body for triggering a dbt run."""

    select: Optional[List[str]] = None
    exclude: Optional[List[str]] = None


class DbtResponse(BaseModel):
    """Result of a dbt invocation."""

    success: bool
    command: str
    message: str
