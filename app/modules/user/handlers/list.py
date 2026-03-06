from typing import Sequence

from redis.asyncio.client import Redis
from sqlmodel import select

from app.adapters.db.models.user import User
from ..queries.list import ListUserQuery
from sqlmodel.ext.asyncio.session import AsyncSession


class ListUserHandler:
    def __init__(self, redis: Redis, session: AsyncSession) -> None:
        self.redis = redis
        self.session = session

    async def __call__(self, query: ListUserQuery) -> Sequence[User]:
        user = (
            await self.session.exec(
                select(User)
                .limit(query.limit)
                .offset(query.offset)
                .order_by(User.created_at)  # type: ignore
            )
        ).all()

        return user
