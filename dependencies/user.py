from typing import Annotated
from uuid import UUID

from fastapi import Depends, HTTPException

from core.security.auth import verify_access_token
from dependencies.redis import RedisDep
from models.user import User

from .oauth2 import Oauth2SchemeDep
from .session import SessionDep


async def get_current_user(
    token: Oauth2SchemeDep,
    session: SessionDep,
    redis: RedisDep,
) -> User:

    # Verify token signature
    claims = await verify_access_token(
        redis,
        token=token,
    )

    # Featch user detail
    user = await session.get(User, UUID(claims["sub"]))
    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired access token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Return current user
    return user


CurrentUserDep = Annotated[User, Depends(get_current_user)]
