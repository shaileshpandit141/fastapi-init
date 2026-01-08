from fastapi import APIRouter

from dependencies.auth.user import ActiveUserDep
from models.user import User
from schemas.user import UserRead

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserRead)
async def read_me(current_user: ActiveUserDep) -> User:
    return current_user
