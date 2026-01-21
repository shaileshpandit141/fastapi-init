from typing import Any, Sequence

from pydantic import BaseModel
from sqlalchemy.exc import IntegrityError
from sqlmodel import SQLModel

from .exceptions import EntityConflictException
from .repository import BaseRepository


class WriteRepositoryMixin[Model: SQLModel, CreateModel: SQLModel | BaseModel](
    BaseRepository[SQLModel]
):
    async def create(
        self,
        *,
        data: CreateModel,
        values: dict[str, Any] | None = None,
        refresh: bool = True,
    ) -> Model:
        try:
            obj = self.model(**data.model_dump(), **(values or {}))
            self.session.add(obj)
            await self.session.commit()

            if refresh:
                await self.session.refresh(obj)

            return obj
        except IntegrityError:
            await self.session.rollback()
            raise EntityConflictException(detail="Resource already exists")

    async def bulk_create(
        self,
        *,
        data: Sequence[CreateModel],
        values: dict[str, Any] | None = None,
        refresh: bool = True,
    ) -> Sequence[Model]:
        objs = [self.model(**item.model_dump(), **(values or {})) for item in data]

        self.session.add_all(objs)
        await self.session.commit()

        if refresh:
            await self.session.refresh(objs)

        return objs
