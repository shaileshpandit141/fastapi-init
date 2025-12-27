from typing import Annotated
from fastapi import Depends, HTTPException
from .session import SessionDep
from .oauth2 import Oauth2SchemeDep
from models.user import User
from core.security.auth import verify_access_token


async def get_current_user(
    token: Oauth2SchemeDep,
    session: SessionDep,
) -> User:

    # Verify token signature
    uuid = verify_access_token(token=token)

    # Featch user detail
    user = await session.get(User, uuid)
    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired access token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Return current user
    return user


CurrentUserDep = Annotated[User, Depends(get_current_user)]
