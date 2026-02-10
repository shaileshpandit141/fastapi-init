import pytest

from core.repositoriesx.commands.create import AsyncSession, Create
from domain.role.models import Role


@pytest.mark.asyncio
@pytest.mark.integration
async def test_create_command(async_session: AsyncSession) -> None:
    data = [Role(name="admin")]
    command = Create(Role, data)
    result = await command.execute(async_session)
    await async_session.commit()

    # Assertions
    assert len(result) == 1
    assert result[0].name == "admin"
