from enum import StrEnum


class UserPerm(StrEnum):
    FULL = "user:*"
    CREATE = "user:create"
    READ = "user:read"
    UPDATE = "user:update"
    DELETE = "user:delete"


class UserRolePerm(StrEnum):
    FULL = "user:role:*"
    ASSIGN = "user:role:assign"
    REVOKE = "user:role:revoke"
    LIST = "user:role:list"


class RolePerm(StrEnum):
    FULL = "role:*"
    CREATE = "role:create"
    READ = "role:read"
    UPDATE = "role:update"
    DELETE = "role:delete"


class PermissionPerm(StrEnum):
    FULL = "permission:*"
    CREATE = "permission:create"
    READ = "permission:read"
    UPDATE = "permission:update"
    DELETE = "permission:delete"


class RolePermissionPerm(StrEnum):
    FULL = "role:permission:*"
    ASSIGN = "role:permission:assign"
    REVOKE = "role:permission:revoke"
    LIST = "role:permission:list"
