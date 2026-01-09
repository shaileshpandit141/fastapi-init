from typing import Annotated, AsyncGenerator, Generator

from fastapi import Depends
from sqlmodel import Session
from sqlmodel.ext.asyncio.session import AsyncSession

from db.connections import sessions


def get_session() -> Generator[Session, None]:
    with sessions.SyncSessionLocal() as session:
        yield session


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with sessions.AsyncSessionLocal() as session:
        yield session


SyncSessionDep = Annotated[AsyncSession, Depends(get_session)]
AsyncSessionDep = Annotated[AsyncSession, Depends(get_async_session)]
