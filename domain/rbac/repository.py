from core.repository.base import AsyncRepository
from domain.rbac.models import Permission, Role, RolePermissionLink, UserRoleLink
from domain.rbac.schemas import (
    PermissionCreate,
    PermissionUpdate,
    RoleCreate,
    RolePermissionLinkCreate,
    RolePermissionLinkUpdate,
    RoleUpdate,
    UserRoleLinkCreate,
    UserRoleLinkUpdate,
)


class RoleRepository(AsyncRepository[Role, RoleCreate, RoleUpdate]):
    pass


class PermissionRepository(
    AsyncRepository[Permission, PermissionCreate, PermissionUpdate]
):
    pass


class RolePermissionLinkRepository(
    AsyncRepository[
        RolePermissionLink, RolePermissionLinkCreate, RolePermissionLinkUpdate
    ]
):
    pass


class UserRoleLinkRepository(
    AsyncRepository[UserRoleLink, UserRoleLinkCreate, UserRoleLinkUpdate]
):
    pass
