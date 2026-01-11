from fastapi import APIRouter

from domain.user.deps import ActiveUserDep
from domain.user.models import User
from domain.user.schemas import UserRead

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.get("/me", response_model=UserRead)
async def read_me(current_user: ActiveUserDep) -> User:
    return current_user
