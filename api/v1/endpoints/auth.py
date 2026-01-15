from fastapi import APIRouter

from domain.auth.deps import AuthServiceDep, OAuth2PasswordRequestFormDep
from domain.auth.schemas import JwtTokenCreate, TokenRead, TokenRefresh, TokenRevoked
from domain.response.schemas import DetailResponse
from domain.user.deps import CurrentUserServiceDep, UserServiceDep
from domain.user.models import User
from domain.user.schemas import UserCreate, UserRead

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
    response_model=TokenRead,
)
async def create_jwt_token(
    form_in: OAuth2PasswordRequestFormDep, auth_service: AuthServiceDep
) -> TokenRead:
    return await auth_service.create_jwt_token(
        form_in=JwtTokenCreate(email=form_in.username, password=form_in.password)
    )


@router.post(
    "/refresh",
    summary="Issue new access token",
    description="Issue new access token by using refresh token.",
    response_model=TokenRead,
)
async def refresh_access_token(
    token_in: TokenRefresh, auth_service: AuthServiceDep
) -> TokenRead:
    return await auth_service.refresh_access_token(token_in=token_in)


@router.post(
    "/revoke",
    summary="Revoke jwt tokens",
    description="Revoke access and refresh tokens.",
    response_model=DetailResponse,
)
async def revoke_token(
    token_in: TokenRevoked, auth_service: AuthServiceDep
) -> DetailResponse:
    return await auth_service.revoke_token(token_in=token_in)


@router.get(
    "/me",
    summary="Get authenticated user info",
    description="Get authenticated user information.",
    response_model=UserRead,
)
async def read_me(current_user_service: CurrentUserServiceDep) -> User:
    return await current_user_service.get_active_user()
