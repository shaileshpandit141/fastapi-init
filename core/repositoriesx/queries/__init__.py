from abc import ABC, abstractmethod

from sqlmodel.ext.asyncio.session import AsyncSession


class RepoQuery[T](ABC):
    """Abstract base class for all repository query."""

    @abstractmethod
    async def execute(self, session: AsyncSession) -> T:
        raise NotImplementedError
