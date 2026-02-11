import pytest

from core.repository.actions.update import AsyncSession, UpdateMany
from domain.role.models import Role
from domain.role.schemas import RoleUpdate


@pytest.mark.asyncio
@pytest.mark.integration
async def test_update_action(async_session: AsyncSession) -> None:
    role = Role(name="developer")
    async_session.add(role)
    await async_session.commit()

    description = "handle developer related action"
    update_data = RoleUpdate(description=description)

    action = UpdateMany(objs=[role], data=update_data)
    updated_objs = await action.execute(async_session)

    await async_session.commit()

    # Assertions
    assert updated_objs[0].description == description
