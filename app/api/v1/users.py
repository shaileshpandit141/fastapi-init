from collections.abc import Sequence
from typing import Annotated

from core.security import hash_password
from db.depends import AsyncSession, get_session
from fastapi import APIRouter, Depends, status
from models.user import CreateUserSchema, User, UserReadSchema
from sqlmodel import select

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", response_model=list[UserReadSchema])
async def list_users(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> Sequence[User]:
    result = await session.exec(select(User))
    return result.all()


@router.post(
    "/",
    response_model=UserReadSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_user(
    payload: CreateUserSchema,
    session: Annotated[AsyncSession, Depends(get_session)],
) -> User:

    user = User(
        email=payload.email,
        password_hash=hash_password(payload.password),
    )

    session.add(user)
    await session.commit()
    await session.refresh(user)

    return user
