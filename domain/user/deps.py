from typing import Annotated

from fastapi import Depends, HTTPException
from sqlalchemy.orm import selectinload
from sqlmodel import select

from core.db.deps import AsyncSessionDep
from domain.auth.deps import Oauth2SchemeDep
from domain.jwt.deps import JwtTokenServiceDep
from domain.jwt.exceptions import JWTError
from domain.rbac.models import UserRoleLink
from infrastructure.cache.redis import RedisDep

from .models import User, UserStatus
from .repository import UserRepository


async def get_user_repository(session: AsyncSessionDep) -> UserRepository:
    return UserRepository(model=User, session=session)


async def get_current_user(
    token_in: Oauth2SchemeDep,
    session: AsyncSessionDep,
    redis: RedisDep,
    token: JwtTokenServiceDep,
) -> User:
    try:
        claims = await token.verify_access_token(token=token_in)
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


UserRepositoryDep = Annotated[UserRepository, Depends(get_user_repository)]

CurrentUserDep = Annotated[User, Depends(get_current_user)]
ActiveUserDep = Annotated[User, Depends(get_active_user)]
