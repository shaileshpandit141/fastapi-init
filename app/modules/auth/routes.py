from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from .dependencies import LoginService, get_login_service
from .schemas.login import UserLogin

router = APIRouter(prefix="/auth", tags=["Auth Endpoints"])


@router.post(
    path="/login",
    summary="Issue new jwt tokens",
    description="Issue new jwt tokens to make requests on protected routes.",
)
async def login(
    form_in: OAuth2PasswordRequestForm = Depends(),
    service: LoginService = Depends(get_login_service),
) -> UserLogin:
    tokens = await service.login(
        email=form_in.username,
        password=form_in.password,
    )

    return UserLogin(**tokens)
