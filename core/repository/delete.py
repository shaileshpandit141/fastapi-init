from logging import getLogger
from typing import Iterable, cast

from sqlmodel import SQLModel, delete

logger = getLogger(__name__)


class DeleteRepositoryMixin[Model: SQLModel]:

    async def delete(self, *, obj: Model) -> None:
        """
        Delete a model instance.

        Parameters
        ----------
        obj
            The model instance to delete.
        """
        await self.session.delete(obj)
        await self.session.commit()

    async def delete_by_id(self, *, id: int) -> None:
        """
        Delete a model instance by primary key.

        Parameters
        ----------
        id
            Primary key of the model.

        Raises
        ------
        NotFoundError
            If the model instance does not exist.
        """
        obj = await self.get_or_raise(id=id)
        await self.delete(obj=obj)

    async def bulk_delete(self, *, ids: Iterable[int]) -> int:
        """
        Delete multiple records by primary key.

        Parameters
        ----------
        ids
            Iterable of primary key values.

        Returns
        -------
        int
            Number of rows deleted.
        """
        stmt = delete(self.model).where(self.model.id.in_(ids))  # type: ignore
        result = await self.session.execute(stmt)
        await self.session.commit()
        return cast(int, result.rowcount) or 0  # type: ignore
