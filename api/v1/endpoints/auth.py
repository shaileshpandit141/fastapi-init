from fastapi import APIRouter

from domain.auth.deps import AuthServiceDep
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


@router.get("/me", response_model=UserRead)
async def read_me(current_user: ActiveUserDep) -> User:
    return current_user
