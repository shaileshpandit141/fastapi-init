from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from .dependencies import JwtTokenService, get_jwt_token_service
from .schemas.login import UserLogin

router = APIRouter(prefix="/auth", tags=["Auth Endpoints"])


@router.post(
    path="/login",
    summary="Issue new jwt tokens",
    description="Issue new jwt tokens to make requests on protected routes.",
    response_model=UserLogin,
)
async def login(
    form_in: OAuth2PasswordRequestForm = Depends(),
    service: JwtTokenService = Depends(get_jwt_token_service),
) -> UserLogin:
    tokens = await service.create_jwt_token(
        email=form_in.username,
        password=form_in.password,
    )

    return UserLogin(**tokens)
