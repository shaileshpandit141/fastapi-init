from logging import getLogger
from typing import Any, Self

from sqlmodel import Session
from sqlmodel.ext.asyncio.session import AsyncSession

from app.shared.exceptions import UnitOfWorkError

# =============================================================================
# Async Unit of Work Context
# =============================================================================


class AsyncUnitOfWork:
    def __init__(self, session: AsyncSession) -> None:
        self._logger = getLogger(self.__class__.__name__)
        self.session = session

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(self, exc_type: Any, exc: Any, tb: Any) -> None:
        try:
            if exc_type:
                self._logger.warning("Rolling back due to exception: %s", exc_type)
                await self.session.rollback()
            else:
                self._logger.debug("Committing transaction")
                await self.session.commit()
        except Exception as exc:
            self._logger.exception("UnitOfWork transaction failed")
            raise UnitOfWorkError("Transaction failed") from exc
        finally:
            await self.session.close()


# =============================================================================
# Sync Unit of Work Context
# =============================================================================


class SyncUnitOfWork:
    def __init__(self, session: Session) -> None:
        self._logger = getLogger(self.__class__.__name__)
        self.session = session

    def __enter__(self) -> Self:
        return self

    def __exit__(self, exc_type: Any, exc: Any, tb: Any) -> None:
        try:
            if exc_type:
                self._logger.warning("Rolling back due to exception: %s", exc_type)
                self.session.rollback()
            else:
                self._logger.debug("Committing transaction")
                self.session.commit()
        except Exception as exc:
            self._logger.exception("UnitOfWork transaction failed")
            raise UnitOfWorkError("Transaction failed") from exc
        finally:
            self.session.close()
