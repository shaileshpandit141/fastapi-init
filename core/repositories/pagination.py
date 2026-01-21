from typing import Sequence

from sqlmodel import SQLModel, func, select

from .repository import BaseRepository


class PaginationMixin[Model: SQLModel](BaseRepository[Model]):
    async def paginate(
        self, *, limit: int = 20, offset: int = 0
    ) -> tuple[Sequence[Model], int]:
        data_stmt = self.base_query().limit(limit).offset(offset)
        count_stmt = select(func.count()).select_from(self.base_query().subquery())

        data = (await self.session.exec(data_stmt)).all()
        total = (await self.session.exec(count_stmt)).one()

        return data, total
