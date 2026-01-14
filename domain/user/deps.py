from typing import Annotated

from fastapi import Depends, HTTPException
from sqlalchemy.orm import selectinload
from sqlmodel import select

from core.db.deps import AsyncSessionDep
from core.security.jwt import JwtTokenManager
from core.security.jwt.exceptions import JwtError
from domain.auth.deps import Oauth2SchemeDep
from domain.rbac.models import UserRoleLink
from domain.user.service import UserService
from infrastructure.cache.redis import RedisDep

from .models import User, UserStatus
from .repository import UserRepository


async def get_current_user(
    token_in: Oauth2SchemeDep, session: AsyncSessionDep, redis: RedisDep
) -> User:

    jwt_token_manager = JwtTokenManager(redis=redis)

    try:
        claims = await jwt_token_manager.verify_access_token(token=token_in)
    except (JwtError, KeyError, ValueError):
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


async def get_active_user(user: Annotated[User, Depends(get_current_user)]) -> User:
    if user.status != UserStatus.ACTIVE:
        raise HTTPException(
            status_code=403,
            detail="Inactive user",
        )
    return user


CurrentUserDep = Annotated[User, Depends(get_current_user)]
ActiveUserDep = Annotated[User, Depends(get_active_user)]


async def get_user_service(session: AsyncSessionDep) -> UserService:
    return UserService(UserRepository(model=User, session=session))


UserServiceDep = Annotated[UserService, Depends(get_user_service)]
