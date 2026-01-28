from fastapi import APIRouter

from core.response.schemas import DetailResponse
from core.swagger import AUTH_READ, PUBLIC_WRITE
from domain.authentication.depends import (
    JwtTokenServiceDep,
    OAuth2PasswordRequestFormDep,
)
from domain.authentication.schemas import (
    JwtTokenCreate,
    JwtTokenRead,
    JwtTokenRefresh,
    JwtTokenRevoked,
)
from domain.user.depends import CurrentUserDep, UserServiceDep
from domain.user.models import User
from domain.user.schemas import UserCreate, UserRead

router = APIRouter(prefix="/auth", tags=["Auth Endpoints"])


@router.post(
    path="/register",
    summary="Register a new user",
    description="Register a new user with email and password.",
    response_model=UserRead,
    responses=PUBLIC_WRITE,
)
async def create_user(user_in: UserCreate, service: UserServiceDep) -> User:
    return await service.create_user(user_in)


@router.post(
    path="/resend-email-otp",
    summary="Resend email verification OTP",
    description=(
        "Resends a one-time password (OTP) to the user's registered email "
        "address for email verification. "
        "This endpoint does not reveal whether the email exists."
    ),
)
async def resend_email_verification_otp() -> None: ...


@router.post(
    path="/verify-email-otp",
    summary="Verify email using OTP",
    description=(
        "Verifies the user's email address using a one-time password (OTP). "
        "The OTP must be valid and not expired."
    ),
)
async def verify_email_otp() -> None: ...


@router.post(
    path="/token",
    summary="Issue new jwt tokens",
    description="Issue new jwt tokens to make requests on protected routes.",
    response_model=JwtTokenRead,
    responses=PUBLIC_WRITE,
)
async def create_jwt_token(
    form_in: OAuth2PasswordRequestFormDep, service: JwtTokenServiceDep
) -> JwtTokenRead:
    return await service.create_jwt_token(
        form_in=JwtTokenCreate(email=form_in.username, password=form_in.password)
    )


@router.post(
    path="/refresh",
    summary="Issue new access token",
    description="Issue new access token by using refresh token.",
    response_model=JwtTokenRead,
    responses=PUBLIC_WRITE,
)
async def refresh_access_token(
    token_in: JwtTokenRefresh, service: JwtTokenServiceDep
) -> JwtTokenRead:
    return await service.refresh_access_token(token_in=token_in)


@router.post(
    path="/revoke",
    summary="Revoke jwt tokens",
    description="Revoke access and refresh tokens.",
    response_model=DetailResponse,
    responses=PUBLIC_WRITE,
)
async def revoke_token(
    token_in: JwtTokenRevoked, service: JwtTokenServiceDep
) -> DetailResponse:
    return await service.revoke_token(token_in=token_in)


@router.get(
    path="/me",
    summary="Get authenticated user info",
    description="Get authenticated user information.",
    response_model=UserRead,
    responses=AUTH_READ,
)
async def read_me(user: CurrentUserDep) -> User:
    return user
