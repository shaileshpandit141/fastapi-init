from abc import ABC, abstractmethod

from sqlmodel.ext.asyncio.session import AsyncSession


class BaseAction[T](ABC):
    """Executable database action returning R."""

    @abstractmethod
    async def execute(self, session: AsyncSession) -> T:
        raise NotImplementedError
