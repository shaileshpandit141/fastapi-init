from abc import ABC, abstractmethod

from sqlmodel.ext.asyncio.session import AsyncSession


class BaseRepoAction[T](ABC):
    """Abstract base class for all repository actions."""

    @abstractmethod
    async def execute(self, session: AsyncSession) -> T:
        pass
