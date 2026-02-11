from logging import getLogger

from sqlmodel.ext.asyncio.session import AsyncSession

from .base import BaseAction


class Repository:
    __slots__ = ("_logger", "session")

    def __init__(self, session: AsyncSession) -> None:
        self._logger = getLogger(self.__class__.__name__)
        self.session = session

    async def execute[T](self, action: BaseAction[T]) -> T:
        self._logger.debug(
            "Executing repository action: %s",
            action.__class__.__name__,
        )
        return await action.execute(self.session)
