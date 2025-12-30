from typing import Annotated
from uuid import UUID

from fastapi import Depends, HTTPException

from core.security.jwt.exceptions import JWTError
from core.security.jwt.verify import verify_access_token
from dependencies.redis import RedisDep
from models.user import User, UserStatus

from .oauth2 import Oauth2SchemeDep
from .session import SessionDep


async def get_current_user(
    token: Oauth2SchemeDep,
    session: SessionDep,
    redis: RedisDep,
) -> User:
    try:
        claims = await verify_access_token(redis, token=token)
        user_id = UUID(claims["id"])
    except (JWTError, KeyError, ValueError):
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired access token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = await session.get(User, user_id)

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid access token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user


async def get_active_user(
    user: Annotated[User, Depends(get_current_user)],
) -> User:
    if user.status != UserStatus.ACTIVE:
        raise HTTPException(
            status_code=403,
            detail="Inactive user",
        )
    return user


CurrentUserDep = Annotated[User, Depends(get_current_user)]

ActiveUserDep = Annotated[User, Depends(get_active_user)]
