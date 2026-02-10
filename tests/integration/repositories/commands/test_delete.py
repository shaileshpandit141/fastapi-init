import pytest

from core.repositoriesx.commands.delete import AsyncSession, Delete
from domain.role.models import Role


@pytest.mark.asyncio
@pytest.mark.integration
async def test_delete_command(async_session: AsyncSession) -> None:
    user = Role(name="manager")
    async_session.add(user)
    await async_session.commit()

    command = Delete([user])
    deleted_count = await command.execute(async_session)
    await async_session.commit()

    # Assertions
    assert deleted_count == 1
