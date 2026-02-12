import pytest

from core.repository.actions.insert import AsyncSession, InsertMany, InsertOne
from domain.role.models import Role


@pytest.mark.asyncio
@pytest.mark.integration
async def test_create_one_action(async_session: AsyncSession) -> None:
    action = InsertOne(model=Role, data=Role(name="role-1"))
    role = await action.execute(async_session)
    await async_session.commit()

    # Assertion
    assert role.name == "role-1"


@pytest.mark.asyncio
@pytest.mark.integration
async def test_create_many_action(async_session: AsyncSession) -> None:
    action = InsertMany(model=Role, data=[Role(name="admin")])
    roles = await action.execute(async_session)
    await async_session.commit()

    # Assertions
    assert len(roles) == 1
    assert roles[0].name == "admin"
