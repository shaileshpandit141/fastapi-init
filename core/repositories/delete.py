from typing import Any, Iterable

from sqlmodel import SQLModel, delete, select

from .exceptions import EntityNotFoundException
from .repository import BaseRepository


class DeleteRepositoryMixin[Model: SQLModel](BaseRepository[Model]):
    async def delete(self, *, obj: Model) -> None:
        await self.session.delete(obj)
        await self.session.commit()

    async def delete_by(self, **filters: Any) -> None:
        stmt = select(self.model).filter_by(**filters)
        obj = (await self.session.exec(stmt)).one_or_none()

        if not obj:
            raise EntityNotFoundException(detail="Resource does not exist")

        await self.delete(obj=obj)

    async def bulk_delete(self, *, ids: Iterable[int]) -> int:
        stmt = delete(self.model).where(
            self.model.id.in_(ids)  # type: ignore[attr-defined]
        )

        result = await self.session.exec(stmt)
        await self.session.commit()

        return result.rowcount or 0

    async def bulk_delete_by(self, *, conditions: Iterable[Any]) -> int:
        stmt = delete(self.model)

        for condition in conditions:
            stmt = stmt.where(condition)

        result = await self.session.exec(stmt)
        await self.session.commit()

        return result.rowcount or 0
