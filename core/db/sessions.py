from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.orm import sessionmaker
from sqlmodel import Session
from sqlmodel.ext.asyncio.session import AsyncSession

from .engines import engines


class SessionFactories:
    def __init__(self) -> None:
        self.session = sessionmaker(
            bind=engines.engine,
            class_=Session,
            autoflush=False,
        )

        self.async_session = async_sessionmaker(
            bind=engines.async_engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )


sessions = SessionFactories()
