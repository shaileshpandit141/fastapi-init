from collections.abc import AsyncGenerator

from .session import Session


async def get_session() -> AsyncGenerator:
    async with Session() as session:
        yield session
