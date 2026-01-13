from fastapi import APIRouter

from domain.auth.deps import AuthServiceDep, OAuth2PasswordRequestFormDep
from domain.auth.schemas import JwtTokenCreate, TokenRead, TokenRefresh, TokenRevoked
from domain.message.schemas import MessageRead
from domain.user.deps import ActiveUserDep
from domain.user.models import User
from domain.user.schemas import UserCreate, UserRead

router = APIRouter(prefix="/auth", tags=["Auth Endpoints"])


@router.post(
    "/signup",
    summary="Create new user",
    description="Create a new user with email and password.",
    response_model=UserRead,
)
async def create_user(user_in: UserCreate, auth_service: AuthServiceDep) -> User:
    return await auth_service.register(user_in=user_in)


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
    response_model=MessageRead,
)
async def revoke_token(
    token_in: TokenRevoked, auth_service: AuthServiceDep
) -> MessageRead:
    return await auth_service.revoke_token(token_in=token_in)


@router.get(
    "/me",
    summary="Get authenticated user info",
    description="Get authenticated user information.",
    response_model=UserRead,
)
async def read_me(current_user: ActiveUserDep) -> User:
    return current_user
