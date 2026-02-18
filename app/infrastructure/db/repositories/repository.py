from logging import getLogger

from sqlmodel.ext.asyncio.session import AsyncSession

from .base import BaseCommand


class Repository:
    __slots__ = ("_logger", "session")

    def __init__(self, session: AsyncSession) -> None:
        self._logger = getLogger(self.__class__.__name__)
        self.session = session

    async def execute[T](self, command: BaseCommand[T]) -> T:
        self._logger.debug(
            "Executing repository command: %s",
            command.__class__.__name__,
        )
        return await command.execute(self.session)
