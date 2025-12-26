from db.engine import engine
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession

LocalSession = async_sessionmaker[AsyncSession](
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession,
)
