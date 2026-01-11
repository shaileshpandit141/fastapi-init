from typing import Annotated, AsyncGenerator, Generator

from fastapi import Depends
from sqlmodel import Session
from sqlmodel.ext.asyncio.session import AsyncSession

from .sessions import sessions


def get_session() -> Generator[Session, None]:
    with sessions.session() as session:
        yield session


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with sessions.async_session() as session:
        yield session


SyncSessionDep = Annotated[AsyncSession, Depends(get_session)]
AsyncSessionDep = Annotated[AsyncSession, Depends(get_async_session)]
