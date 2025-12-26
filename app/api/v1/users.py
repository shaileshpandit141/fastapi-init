from collections.abc import Sequence
from typing import Annotated

from db.depends import get_session
from fastapi import APIRouter, Depends, status
from models.user import User
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", response_model=list[User])
async def list_users(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> Sequence[User]:
    result = await session.exec(select(User))
    return result.all()


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(
    user: User,
    session: Annotated[AsyncSession, Depends(get_session)],
) -> User:
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user
