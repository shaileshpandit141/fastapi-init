from abc import ABC

from sqlmodel import SQLModel, select
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel.sql._expression_select_cls import SelectOfScalar


class BaseRepository[Model: SQLModel](ABC):
    """
    Abstract base class for SQLModel repositories.

    This class provides the minimal shared infrastructure required by all
    repository mixins, including access to the database session and the
    managed SQLModel type. It does not implement any CRUD behavior directly
    and is intended to be composed via mixins.

    Type Parameters
    ---------------
    Model
        The SQLModel table type managed by the repository.
    """

    __slots__ = ("model", "session")

    def __init__(self, *, model: type[Model], session: AsyncSession) -> None:
        """
        Initialize the repository with a model and an async database session.

        Parameters
        ----------
        model
            The SQLModel table class associated with this repository.
        session
            An active asynchronous SQLModel session.
        """
        self.model = model
        self.session = session

    def base_query(self) -> SelectOfScalar[Model]:
        """
        Create a base SELECT query for the repository's model.

        This method serves as a common starting point for read operations
        and may be extended or modified by repository mixins.

        Returns
        -------
        SelectOfScalar[Model]
            A SQLModel SELECT statement targeting the repository model.
        """
        return select(self.model)
