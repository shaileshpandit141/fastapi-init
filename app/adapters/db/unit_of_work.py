from logging import getLogger
from typing import Any, Self

from sqlmodel import Session
from sqlmodel.ext.asyncio.session import AsyncSession

# =============================================================================
# Async Unit of Work Context
# =============================================================================


class AsyncUnitOfWork:
    def __init__(self, session: AsyncSession) -> None:
        self._logger = getLogger(self.__class__.__name__)
        self.session = session

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(self, exc_type: Any, *_) -> None:
        try:
            if exc_type:
                self._logger.warning("Rolling back due to exception: %s", exc_type)
                await self.rollback()
            else:
                self._logger.debug("Committing transaction")
                await self.commit()
        except Exception as exc:
            self._logger.exception("UnitOfWork transaction failed")
            raise exc
        finally:
            await self.session.close()

    async def commit(self) -> None:
        await self.session.commit()

    async def rollback(self) -> None:
        await self.session.rollback()


# =============================================================================
# Sync Unit of Work Context
# =============================================================================


class SyncUnitOfWork:
    def __init__(self, session: Session) -> None:
        self._logger = getLogger(self.__class__.__name__)
        self.session = session

    def __enter__(self) -> Self:
        return self

    def __exit__(self, exc_type: Any, *_) -> None:
        try:
            if exc_type:
                self._logger.warning("Rolling back due to exception: %s", exc_type)
                self.rollback()
            else:
                self._logger.debug("Committing transaction")
                self.commit()
        except Exception as exc:
            self._logger.exception("UnitOfWork transaction failed")
            raise exc
        finally:
            self.session.close()

    def commit(self) -> None:
        self.session.commit()

    def rollback(self) -> None:
        self.session.rollback()
