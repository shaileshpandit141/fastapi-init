from logging import getLogger

from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from .commands import RepoCommand
from .queries import RepoQuery

# =============================================================================
# Main Repository
# =============================================================================


class Repository[T: SQLModel]:
    __slots__ = ("_logger", "session")

    def __init__(self, session: AsyncSession) -> None:
        self._logger = getLogger(self.__class__.__name__)
        self.session = session

    async def execute(self, command: RepoCommand[T]) -> T:
        self._logger.debug(
            "Executing repo command: %s",
            command.__class__.__name__,
        )
        return await command.execute(self.session)

    async def query(self, query: RepoQuery[T]) -> T:
        self._logger.debug(
            "Executing repo query: %s",
            query.__class__.__name__,
        )
        return await query.execute(self.session)
