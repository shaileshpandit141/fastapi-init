from typing import Annotated, AsyncGenerator, Generator

from fastapi import Depends
from sqlmodel import Session
from sqlmodel.ext.asyncio.session import AsyncSession

from .sessions import async_session, session


def get_session() -> Generator[Session, None]:
    with session() as sessionx:
        yield sessionx


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
AsyncSessionDep = Annotated[AsyncSession, Depends(get_async_session)]
