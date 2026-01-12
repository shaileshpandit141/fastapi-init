from fastapi import APIRouter

from domain.auth.deps import AuthServiceDep, OAuth2PasswordRequestFormDep
from domain.auth.schemas import TokenRead, TokenRefresh
from domain.user.deps import ActiveUserDep
from domain.user.models import User
from domain.user.schemas import UserCreate, UserRead

router = APIRouter(prefix="/auth", tags=["Auth Endpoints"])


@router.post(
    "/signup",
    summary="Create new user",
    description="Create a new user with email and password",
    response_model=UserRead,
)
async def create_user(user_in: UserCreate, auth_service: AuthServiceDep) -> User:
    return await auth_service.signup(user_in=user_in)


@router.post(
    "/token",
    summary="Get new jwt tokens",
    description="Get new jwt tokens to make requests on protected routes",
    response_model=TokenRead,
)
async def create_access_token(
    form_in: OAuth2PasswordRequestFormDep, auth_service: AuthServiceDep
) -> TokenRead:
    return await auth_service.signin(
        form_in=UserCreate(email=form_in.username, password=form_in.password)
    )


@router.post(
    "/refresh",
    summary="Get new access token",
    description="Get new access token by using refresh token",
    response_model=TokenRead,
)
async def refresh_access_token(
    token_in: TokenRefresh, auth_service: AuthServiceDep
) -> TokenRead:
    return await auth_service.refresh_access_token(token_in=token_in)


@router.get("/me", response_model=UserRead)
async def read_me(current_user: ActiveUserDep) -> User:
    return current_user
