from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm

from core.db.deps import AsyncSessionDep
from domain.jwt.deps import JwtTokenServiceDep
from domain.password.deps import PasswordServiceDep

from .schemas import oauth2_scheme
from .service import AuthService


async def get_auth_service(
    jwt_token_service: JwtTokenServiceDep,
    password: PasswordServiceDep,
    session: AsyncSessionDep,
) -> AuthService:
    return AuthService(token=jwt_token_service, password=password, session=session)


AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]
Oauth2SchemeDep = Annotated[str, Depends(oauth2_scheme)]
OAuth2PasswordRequestFormDep = Annotated[OAuth2PasswordRequestForm, Depends()]
