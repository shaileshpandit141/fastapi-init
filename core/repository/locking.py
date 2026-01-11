from logging import getLogger

from sqlmodel import SQLModel, select

from .exceptions import NotFoundError

logger = getLogger(__name__)


class LockingRepositoryMixin[Model: SQLModel]:

    async def lock_for_update(self, *, id: int) -> Model:
        """
        Retrieve a record by primary key and lock it for update.

        This issues a SELECT ... FOR UPDATE statement.

        Parameters
        ----------
        id
            Primary key of the model.

        Returns
        -------
        Model
            The locked model instance.

        Raises
        ------
        NotFoundError
            If the model instance does not exist.
        """
        stmt = select(self.model).where(self.model.id == id).with_for_update()  # type: ignore
        obj = (await self.session.execute(stmt)).scalar_one_or_none()

        if not obj:
            raise NotFoundError()

        return obj
