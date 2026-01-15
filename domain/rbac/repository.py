from core.repository.base import AsyncRepository
from domain.rbac.models import Permission, Role, RolePermission, UserRole
from domain.rbac.schemas import (
    PermissionCreate,
    PermissionUpdate,
    RoleCreate,
    RolePermissionCreate,
    RolePermissionUpdate,
    RoleUpdate,
    UserRoleCreate,
    UserRoleUpdate,
)


class RoleRepository(AsyncRepository[Role, RoleCreate, RoleUpdate]):
    pass


class PermissionRepository(
    AsyncRepository[Permission, PermissionCreate, PermissionUpdate]
):
    pass


class RolePermissionRepository(
    AsyncRepository[RolePermission, RolePermissionCreate, RolePermissionUpdate]
):
    pass


class UserRoleRepository(AsyncRepository[UserRole, UserRoleCreate, UserRoleUpdate]):
    pass
