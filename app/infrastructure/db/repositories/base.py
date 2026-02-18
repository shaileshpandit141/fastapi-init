from abc import ABC, abstractmethod

from sqlmodel.ext.asyncio.session import AsyncSession


class BaseCommand[T](ABC):
    """Executable database cammond returning R."""

    @abstractmethod
    async def execute(self, session: AsyncSession) -> T:
        raise NotImplementedError
