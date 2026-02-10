import pytest
from sqlmodel import SQLModel

from core.db.mixins import IntIDMixin
from core.repositoriesx.commands.create import AsyncSession, Create


class User(IntIDMixin, SQLModel, table=True):
    name: str
    email: str


@pytest.mark.asyncio
@pytest.mark.integration
async def test_create_command(async_session: AsyncSession) -> None:
    data = [User(name="Alice", email="alice@test.com")]
    command = Create(User, data)
    result = await command.execute(async_session)
    await async_session.commit()

    # Assertions
    assert len(result) == 1
    assert result[0].name == "Alice"
    assert result[0].email == "alice@test.com"
