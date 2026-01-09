from typing import Annotated

from fastapi import Depends, HTTPException
from sqlalchemy.orm import selectinload
from sqlmodel import select

from core.security.jwt.exceptions import JWTError
from core.security.jwt.verify import verify_access_token
from dependencies.auth.oauth2 import Oauth2SchemeDep
from dependencies.cache.redis import RedisDep
from dependencies.connections.sessions import AsyncSessionDep
from models.user import User, UserStatus
from models.user_role_link import UserRoleLink


async def get_current_user(
    token: Oauth2SchemeDep, session: AsyncSessionDep, redis: RedisDep
) -> User:
    try:
        claims = await verify_access_token(redis, token=token)
    except (JWTError, KeyError, ValueError):
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired access token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    stmt = (
        select(User)
        .where(User.id == claims["id"])
        .options(
            selectinload(User.roles).selectinload(  # type: ignore[arg-type]
                UserRoleLink.role  # type: ignore[arg-type]
            )
        )
    )

    result = await session.exec(stmt)
    user = result.one_or_none()

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
