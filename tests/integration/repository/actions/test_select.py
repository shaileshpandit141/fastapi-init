import pytest

from core.repository.actions.select import AsyncSession, SelectMany, SelectOne
from domain.role.models import Role


@pytest.mark.asyncio
@pytest.mark.integration
async def test_select_one_action(async_session: AsyncSession) -> None:
    roles = [Role(name="role-4"), Role(name="role-5")]

    async_session.add_all(roles)
    await async_session.commit()

    action = SelectOne(model=Role, where=[Role.name == "role-4"])
    role = await action.execute(async_session)

    # Assertion
    assert role.name == "role-4"  # type: ignore


@pytest.mark.asyncio
@pytest.mark.integration
async def test_select_many_action(async_session: AsyncSession) -> None:
    action = SelectMany(model=Role, where=[Role.name == "role-5"])
    roles = await action.execute(async_session)

    # Assertions
    assert len(roles) > 0
    assert roles[0].name == "role-5"
