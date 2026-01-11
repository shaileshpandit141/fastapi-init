from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import SQLModel


class AsyncBaseRepository[Model: SQLModel]:
    def __init__(self, *, session: AsyncSession, model: type[Model]) -> None:
        """
        Initialize the CRUD service.

        Parameters
        ----------
        session
            An active SQLModel AsyncSession.
        model
            The SQLModel managed by this service.
        """
        self.session = session
        self.model = model
