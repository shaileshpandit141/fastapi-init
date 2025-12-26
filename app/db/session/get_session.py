from collections.abc import AsyncGenerator

from .loacl_session import LocalSession


async def get_session() -> AsyncGenerator:
    async with LocalSession() as session:
        yield session
