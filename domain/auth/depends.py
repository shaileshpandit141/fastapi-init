from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm

from core.db.deps import AsyncSessionDep
from infrastructure.cache.redis import RedisDep

from .schemas import oauth2_scheme
from .service import AuthService


async def get_auth_service(session: AsyncSessionDep, redis: RedisDep) -> AuthService:
    return AuthService(session=session, redis=redis)


AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]
Oauth2SchemeDep = Annotated[str, Depends(oauth2_scheme)]
OAuth2PasswordRequestFormDep = Annotated[OAuth2PasswordRequestForm, Depends()]
