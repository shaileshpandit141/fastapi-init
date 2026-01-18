from typing import Annotated, AsyncGenerator

from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from ..sessions.async_session import async_session


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session


AsyncSessionDep = Annotated[AsyncSession, Depends(get_async_session)]
