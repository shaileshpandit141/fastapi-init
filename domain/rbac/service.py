from typing import Sequence

from fastapi import HTTPException, status

from core.repository.exceptions import ConflictError, NotFoundError
from domain.rbac.schemas import PermissionCreate, PermissionUpdate

from .models import Permission, Role, RolePermission, UserRole
from .repository import (
    PermissionRepository,
    RolePermissionRepository,
    RoleRepository,
    UserRoleRepository,
)
from .schemas import (
    RoleCreate,
    RolePermissionCreate,
    RolePermissionUpdate,
    RoleUpdate,
    UserRoleCreate,
)

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


# === Role Permission Service ===


class RolePermissionService:
    def __init__(self, role_permission_repo: RolePermissionRepository) -> None:
        self.role_permission_repo = role_permission_repo

    async def create_role_permission(
        self, role_permission_in: RolePermissionCreate
    ) -> RolePermission:
        try:
            role_permission = await self.role_permission_repo.create(
                data=role_permission_in,
            )
        except ConflictError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Role permission already exist",
            )

        return role_permission

    async def get_role_permission(self, role_permission_id: int) -> RolePermission:
        try:
            role_permission = await self.role_permission_repo.get_or_raise(
                id=role_permission_id
            )
        except NotFoundError:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Role permission does not exist",
            )

        return role_permission

    async def list_role_permission(
        self, limit: int = 20, offset: int = 0
    ) -> Sequence[RolePermission]:
        role_permissions = await self.role_permission_repo.list(
            limit=limit,
            offset=offset,
        )

        return role_permissions

    async def update_role_permission(
        self, role_permission_id: int, role_permission_in: RolePermissionUpdate
    ) -> RolePermission:
        db_role_permission = await self.get_role_permission(role_permission_id)

        role_permission = await self.role_permission_repo.update(
            obj=db_role_permission,
            data=role_permission_in,
        )

        return role_permission

    async def delete_role_permission(self, role_permission_id: int) -> None:
        try:
            await self.role_permission_repo.delete_by_id(id=role_permission_id)
        except NotFoundError:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Role permission does not exist",
            )


# === User Role Service ===


class UserRoleService:
    def __init__(self, user_role_repo: UserRoleRepository) -> None:
        self.user_role_repo = user_role_repo

    async def create_user_role(self, user_role_in: UserRoleCreate) -> UserRole:
        try:
            user_role = await self.user_role_repo.create(
                data=user_role_in,
            )
        except ConflictError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User role already exist",
            )

        return user_role

    async def get_user_role(self, user_role_id: int) -> UserRole:
        try:
            user_role = await self.user_role_repo.get_or_raise(id=user_role_id)
        except NotFoundError:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User role does not exist",
            )

        return user_role
