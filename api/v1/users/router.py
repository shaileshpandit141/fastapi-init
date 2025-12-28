from fastapi import APIRouter

from dependencies.user import CurrentUserDep
from models.user import User
from schemas.user import UserRead

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserRead)
async def read_me(current_user: CurrentUserDep) -> User:
    return current_user
