from logging import getLogger

from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from .repo_actions.base import BaseRepoAction

# =============================================================================
# Base Repository
# =============================================================================


class BaseRepository[T: SQLModel]():
    __slots__ = ("_logger", "model", "session")

    def __init__(self, model: type[SQLModel], session: AsyncSession) -> None:
        self._logger = getLogger(self.__class__.__name__)
        self.model = model
        self.session = session

    async def execute(self, repo_actions: BaseRepoAction[T]) -> T:
        try:
            self._logger.debug("Executing action: %s", repo_actions)
            result = await repo_actions.execute(self.session)
            self._logger.info("Repository action executed successfully: %s", result)
            return result
        except Exception as exc:
            self._logger.error("Error executing action: %s", exc_info=exc)
            await self.session.rollback()
            raise
