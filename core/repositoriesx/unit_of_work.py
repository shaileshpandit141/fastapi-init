from logging import getLogger
from typing import Any, Self

from sqlmodel import SQLModel

from ..repositoriesx import Repository
from .exceptions import UnitOfWorkError


class UnitOfWork[T: SQLModel]:
    def __init__(self, repo: Repository[T]) -> None:
        self._logger = getLogger(self.__class__.__name__)
        self.repo = repo

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(self, exc_type: Any, exc: Any, tb: Any) -> None:
        try:
            if exc_type:
                self._logger.warning("Rolling back due to exception: %s", exc_type)
                await self.repo.session.rollback()
            else:
                self._logger.debug("Committing transaction")
                await self.repo.session.commit()
        except Exception as exc:
            self._logger.warning("UnitOfWork transaction failed", exc_info=exc)
            raise UnitOfWorkError("UnitOfWork transaction failed")
