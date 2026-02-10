from abc import ABC, abstractmethod

from sqlmodel.ext.asyncio.session import AsyncSession


class RepoCommand[T](ABC):
    """Abstract base class for all repository command."""

    @abstractmethod
    async def execute(self, session: AsyncSession) -> T:
        raise NotImplementedError
