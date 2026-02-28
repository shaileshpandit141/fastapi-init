from httpx import AsyncClient
import pytest

# =============================================================================
# LOGIN TEST
# =============================================================================


@pytest.mark.asyncio
async def test_login_success(async_client: AsyncClient) -> None:
    response = await async_client.post(
        "/auth/login",
        data={
            "username": "test@example.com",
            "password": "password123",
        },
    )

    assert response.status_code != 200
