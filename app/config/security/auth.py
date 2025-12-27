from datetime import datetime, timedelta, timezone
from uuid import UUID
from jose import JWTError, jwt
from ..settings import settings
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer


def get_utc_now() -> datetime:
    return datetime.now(timezone.utc)


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/token",
    description="Use email as the username field",
)


def create_access_token(
    data: dict[str, str | int | datetime],
    expires_delta: timedelta | None = None,
) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = get_utc_now() + expires_delta
    else:
        expire = get_utc_now() + timedelta(
            minutes=settings.access_token_expire_minutes,
        )
    to_encode.update({"type": "access", "exp": expire})
    encoded_jwt = jwt.encode(
        to_encode,
        settings.access_secret_key,
        algorithm=settings.algorithm,
    )

    return encoded_jwt


def verify_access_token(token: str) -> UUID:
    credentials_exception = HTTPException(
        status_code=401,
        detail="Invalid or expired access token",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token,
            settings.access_secret_key,
            algorithms=[settings.algorithm],
        )
        if payload.get("type") != "access":
            raise HTTPException(
                status_code=401,
                detail="Invalid token type",
            )

        # Get auth subject detail
        uuid: str | None = payload.get("sub")
        if uuid is None:
            raise credentials_exception

        # Return UUID instance
        return UUID(uuid)
    except JWTError:
        raise credentials_exception


def create_refresh_token(
    data: dict[str, str | int | datetime],
    expires_delta: timedelta | None = None,
) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = get_utc_now() + expires_delta
    else:
        expire = get_utc_now() + timedelta(
            minutes=settings.refresh_token_expire_minutes,
        )
    to_encode.update({"type": "refresh", "exp": expire})
    encoded_jwt = jwt.encode(
        to_encode,
        settings.refresh_secret_key,
        algorithm=settings.algorithm,
    )

    return encoded_jwt


def verify_refresh_token(token: str) -> UUID:
    credentials_exception = HTTPException(
        status_code=401,
        detail="Invalid or expired refresh token",
    )

    try:
        payload = jwt.decode(
            token,
            settings.refresh_secret_key,
            algorithms=[settings.algorithm],
        )
        if payload.get("type") != "refresh":
            raise HTTPException(
                status_code=401,
                detail="Invalid token type",
            )

        # Get auth subject detail
        uuid: str | None = payload.get("sub")
        if uuid is None:
            raise credentials_exception

        # Return UUID instance
        return UUID(uuid)
    except JWTError:
        raise credentials_exception
