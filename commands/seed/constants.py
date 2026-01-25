from domain.permission.constants import (
    PermissionPerm,
    RolePerm,
    RolePermissionPerm,
    UserPerm,
    UserRolePerm,
)
from domain.role.constants import RoleType

ROLES: list[tuple[str, str]] = RoleType.choices()

PERMISSIONS: list[tuple[str, str]] = [
    *UserPerm.choices(),
    *UserRolePerm.choices(),
    *RolePerm.choices(),
    *PermissionPerm.choices(),
    *RolePermissionPerm.choices(),
]
