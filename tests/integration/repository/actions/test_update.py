import pytest

from core.repository.actions.select import SelectMany, SelectOne
from core.repository.actions.update import AsyncSession, UpdateMany, UpdateOne
from domain.role.models import Role
from domain.role.schemas import RoleUpdate


@pytest.mark.asyncio
@pytest.mark.integration
async def test_update_one_action(async_session: AsyncSession) -> None:
    action = SelectOne(model=Role, where=[Role.name == "role-5"])
    role = await action.execute(async_session)

    if role is None:
        return None

    description = "this is role description."
    update_data = RoleUpdate(description=description)

    actionx = UpdateOne(obj=role, data=update_data)
    updated_role = await actionx.execute(async_session)

    await async_session.commit()

    # Assertions
    assert updated_role.description == description


@pytest.mark.asyncio
@pytest.mark.integration
async def test_update_many_action(async_session: AsyncSession) -> None:
    action = SelectMany(model=Role, where=[Role.name == "role-5"])
    roles = await action.execute(async_session)

    description = "this is role description."
    update_data = RoleUpdate(description=description)

    actionx = UpdateMany(objs=roles, data=update_data)
    updated_roles = await actionx.execute(async_session)

    await async_session.commit()

    # Assertion
    assert updated_roles[0].description == description
