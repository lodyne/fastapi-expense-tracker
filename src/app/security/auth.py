"""Authentication helpers for API users."""

from __future__ import annotations

import os
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from .jwt import create_access_token, decode_access_token


OAUTH2_SCHEME = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")


def _credentials() -> tuple[str, str]:
    username = os.getenv("API_USERNAME", "admin")
    password = os.getenv("API_PASSWORD", "admin")
    return username, password


def authenticate_user(username: str, password: str) -> bool:
    stored_username, stored_password = _credentials()
    return username == stored_username and password == stored_password


def create_token_for_user(username: str) -> str:
    return create_access_token({"sub": username})


def get_current_user(token: str = Depends(OAUTH2_SCHEME)) -> dict[str, str]:
    payload = decode_access_token(token)
    username = payload.get("sub")
    if not username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {"username": username}
