"""JWT helper utilities using PyJWT."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any, Dict

import os
import jwt
from fastapi import HTTPException, status


def _require_env(key: str, default: str | None = None) -> str:
    """Fetch an environment variable or raise if it is missing."""
    value = os.getenv(key, default)
    if value is None:
        raise RuntimeError(f"Environment variable '{key}' is required for JWT configuration")
    return value


SECRET_KEY = _require_env("JWT_SECRET_KEY", "change-me")
ALGORITHM = _require_env("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(_require_env("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", "30"))


def create_access_token(subject: Dict[str, Any], expires_delta: timedelta | None = None) -> str:
    """Create a signed JWT access token for the given subject."""
    to_encode = subject.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str) -> Dict[str, Any]:
    """Decode the JWT token and return its payload if valid."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.PyJWTError as exc:  # catch all decode / expiration issues
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc
    return payload
