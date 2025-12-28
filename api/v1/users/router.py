from fastapi import APIRouter

from dependencies.user import CurrentUserDep
from models.user import User
from schemas.user import UserResponse

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserResponse)
async def read_me(current_user: CurrentUserDep) -> User:
    return current_user
