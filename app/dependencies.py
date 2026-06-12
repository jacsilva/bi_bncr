"""Authentication and authorization dependencies for BI NBCR API.

Provides dependency injection functions for API key verification and
authenticated database sessions.
"""

import os

from fastapi import Depends, Header, HTTPException
from sqlalchemy.orm import Session

from app.database.connection import get_db

API_KEY = os.getenv("API_KEY", "1234")


def verify_api_key(x_api_key: str = Header(..., alias="X-API-Key")) -> str:
    """Verify API key from request header.

    Args:
        x_api_key: API key provided in X-API-Key header.

    Returns:
        The validated API key.

    Raises:
        HTTPException: If API key is invalid or missing.
    """
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="API Key inválida")
    return x_api_key


def get_authenticated_db(db: Session = Depends(get_db)) -> Session:
    """Provide a database session behind API-key authentication.

    Args:
        db: Database session from get_db dependency.

    Returns:
        Authenticated database session.
    """
    return db
