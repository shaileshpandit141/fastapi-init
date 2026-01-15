from fastapi import HTTPException, status

from core.repository.exceptions import ConflictError

from .models import Role
from .repository import RoleRepository
from .schemas import RoleCreate

# === Role Repository ===


class RoleService:
    def __init__(self, role_repo: RoleRepository) -> None:
        self.role_repo = role_repo

    async def create_role(self, role_in: RoleCreate) -> Role:
        try:
            role = await self.role_repo.create(data=role_in)
        except ConflictError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="This role is exist"
            )

        return role
