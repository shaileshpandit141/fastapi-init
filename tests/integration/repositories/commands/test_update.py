import pytest

from core.repositoriesx.commands.update import AsyncSession, Update
from domain.role.models import Role
from domain.role.schemas import RoleUpdate


@pytest.mark.asyncio
@pytest.mark.integration
async def test_update_command(async_session: AsyncSession) -> None:
    user = Role(name="developer")
    async_session.add(user)
    await async_session.commit()

    description = "handle developer related action"
    update_data = RoleUpdate(description=description)
    command = Update([user], update_data)
    updated_objs = await command.execute(async_session)

    await async_session.commit()

    # Assertions
    assert updated_objs[0].description == description
