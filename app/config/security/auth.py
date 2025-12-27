from datetime import datetime, timedelta, timezone
from typing import Annotated
from uuid import UUID
from jose import JWTError, jwt
from ..settings import settings
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from models.user import User
from db.session import AsyncSession, get_session


def get_utc_now() -> datetime:
    return datetime.now(timezone.utc)


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="token",
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
        expire = get_utc_now() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode,
        settings.secret_key,
        algorithm=settings.algorithm,
    )
    return encoded_jwt


async def get_current_user(
    session: Annotated[AsyncSession, Depends(get_session)],
    token: str = Depends(oauth2_scheme),
) -> User:
    credentials_exception = HTTPException(
        status_code=401,
        detail="Invalid or expired access token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.algorithm],
        )

        # Get auth subject detail
        uuid: str | None = UUID(payload.get("sub"))
        if uuid is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    # Featch user detail
    user = await session.get(User, uuid)
    if user is None:
        raise credentials_exception

    return user
