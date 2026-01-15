from typing import Sequence

from fastapi import HTTPException, status

from core.repository.exceptions import ConflictError, NotFoundError
from domain.rbac.schemas import PermissionCreate, PermissionUpdate

from .models import Permission, Role
from .repository import PermissionRepository, RoleRepository
from .schemas import RoleCreate, RoleUpdate

# === Role Service ===


class RoleService:
    def __init__(self, role_repo: RoleRepository) -> None:
        self.role_repo = role_repo

    async def create_role(self, role_in: RoleCreate) -> Role:
        try:
            role = await self.role_repo.create(data=role_in)
        except ConflictError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Role already exist"
            )

        return role

    async def get_role(self, role_id: int) -> Role:
        try:
            role = await self.role_repo.get_or_raise(id=role_id)
        except NotFoundError:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Role does not exist"
            )

        return role

    async def list_role(self, limit: int = 20, offset: int = 0) -> Sequence[Role]:
        roles = await self.role_repo.list(
            limit=limit,
            offset=offset,
        )
        return roles

    async def update_role(self, role_id: int, role_in: RoleUpdate) -> Role:
        db_role = await self.get_role(role_id)

        role = await self.role_repo.update(
            obj=db_role,
            data=role_in,
        )

        return role

    async def delete_role(self, role_in: int) -> None:
        try:
            await self.role_repo.delete_by_id(id=role_in)
        except NotFoundError:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Role does not exist"
            )


# === Permission Service ===


class PermissionService:
    def __init__(self, permission_repo: PermissionRepository) -> None:
        self.permission_repo = permission_repo

    async def create_permission(self, permission_in: PermissionCreate) -> Permission:
        try:
            permission = await self.permission_repo.create(data=permission_in)
        except ConflictError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Permission already exist",
            )

        return permission

    async def get_permission(self, permission_id: int) -> Permission:
        try:
            permission = await self.permission_repo.get_or_raise(id=permission_id)
        except NotFoundError:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Permission does not exist",
            )

        return permission

    async def list_permission(
        self, limit: int = 20, offset: int = 0
    ) -> Sequence[Permission]:
        permissions = await self.permission_repo.list(
            limit=limit,
            offset=offset,
        )

        return permissions

    async def update_permission(
        self, permission_id: int, permission_in: PermissionUpdate
    ) -> Permission:
        db_permission = await self.get_permission(permission_id)

        permission = await self.permission_repo.update(
            obj=db_permission,
            data=permission_in,
        )

        return permission

    async def delete_permission(self, permission_id: int) -> None:
        try:
            await self.permission_repo.delete_by_id(id=permission_id)
        except NotFoundError:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Permission does not exist",
            )
