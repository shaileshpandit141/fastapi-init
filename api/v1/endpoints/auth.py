from fastapi import APIRouter

from core.response import DetailResponse
from domain.auth.depends.jwt_token import JwtTokenServiceDep
from domain.auth.depends.oauth2 import OAuth2PasswordRequestFormDep
from domain.auth.schemas.jwt_token import (
    JwtTokenCreate,
    JwtTokenRead,
    JwtTokenRefresh,
    JwtTokenRevoked,
)
from domain.user.depends.current_user import CurrentUserServiceDep
from domain.user.depends.user import UserServiceDep
from domain.user.models import User
from domain.user.schemas.user import UserCreate, UserRead

router = APIRouter(prefix="/auth", tags=["Auth Endpoints"])


@router.post(
    "/register",
    summary="Register a new user",
    description="Register a new user with email and password.",
    response_model=UserRead,
)
async def create_user(user_in: UserCreate, user_service: UserServiceDep) -> User:
    return await user_service.create_user(user_in)


@router.post(
    "/token",
    summary="Issue new jwt tokens",
    description="Issue new jwt tokens to make requests on protected routes.",
    response_model=JwtTokenRead,
)
async def create_jwt_token(
    form_in: OAuth2PasswordRequestFormDep, jwt_token_service: JwtTokenServiceDep
) -> JwtTokenRead:
    return await jwt_token_service.create_jwt_token(
        form_in=JwtTokenCreate(email=form_in.username, password=form_in.password)
    )


@router.post(
    "/refresh",
    summary="Issue new access token",
    description="Issue new access token by using refresh token.",
    response_model=JwtTokenRead,
)
async def refresh_access_token(
    token_in: JwtTokenRefresh, jwt_token_service: JwtTokenServiceDep
) -> JwtTokenRead:
    return await jwt_token_service.refresh_access_token(token_in=token_in)


@router.post(
    "/revoke",
    summary="Revoke jwt tokens",
    description="Revoke access and refresh tokens.",
    response_model=DetailResponse,
)
async def revoke_token(
    token_in: JwtTokenRevoked, jwt_token_service: JwtTokenServiceDep
) -> DetailResponse:
    return await jwt_token_service.revoke_token(token_in=token_in)


@router.get(
    "/me",
    summary="Get authenticated user info",
    description="Get authenticated user information.",
    response_model=UserRead,
)
async def read_me(current_user_service: CurrentUserServiceDep) -> User:
    return await current_user_service.get_active_user()
