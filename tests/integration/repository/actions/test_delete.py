import pytest

from core.repository.actions.delete import AsyncSession, DeleteMany, DeleteOne
from domain.role.models import Role


@pytest.mark.asyncio
@pytest.mark.integration
async def test_delete_one_action(async_session: AsyncSession) -> None:
    role = Role(name="role-2")
    async_session.add(role)
    await async_session.commit()

    action = DeleteOne(obj=role)
    deleted_count = await action.execute(async_session)
    await async_session.commit()

    # Assertion
    assert deleted_count == 1


@pytest.mark.asyncio
@pytest.mark.integration
async def test_delete_many_action(async_session: AsyncSession) -> None:
    role = Role(name="role-3")
    async_session.add(role)
    await async_session.commit()

    action = DeleteMany(objs=[role])
    deleted_count = await action.execute(async_session)
    await async_session.commit()

    # Assertion
    assert deleted_count == 1
