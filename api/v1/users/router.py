from fastapi import APIRouter

from dependencies.user import ActiveUserDep
from models.user import User
from schemas.user import UserResponse

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserResponse)
async def read_me(current_user: ActiveUserDep) -> User:
    return current_user
