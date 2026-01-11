from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm

from domain.password.deps import PasswordServiceDep
from domain.token.deps import JwtTokenServiceDep

from .schemas import oauth2_scheme
from .service import AuthService


async def get_auth_service(
    jwt_token_service: JwtTokenServiceDep, password: PasswordServiceDep
) -> AuthService:
    return AuthService(token=jwt_token_service, password=password)


AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]
Oauth2SchemeDep = Annotated[str, Depends(oauth2_scheme)]
OAuth2PasswordRequestFormDep = Annotated[OAuth2PasswordRequestForm, Depends()]
