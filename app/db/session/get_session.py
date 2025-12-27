from typing import AsyncGenerator

from sqlmodel.ext.asyncio.session import AsyncSession

from .session import Session


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with Session() as session:
        yield session
