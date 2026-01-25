from core.enums import DescribedEnum


class UserPerm(DescribedEnum):
    FULL = ("user:*", "full access to users")
    CREATE = ("user:create", "create user")
    READ = ("user:read", "read user")
    UPDATE = ("user:update", "update user")
    DELETE = ("user:delete", "delete user")


class UserRolePerm(DescribedEnum):
    FULL = ("user:role:*", "full access to user roles")
    ASSIGN = ("user:role:assign", "assign role to user")
    REVOKE = ("user:role:revoke", "revoke role from user")
    LIST = ("user:role:list", "list user roles")


class RolePerm(DescribedEnum):
    FULL = ("role:*", "full access to roles")
    CREATE = ("role:create", "create role")
    READ = ("role:read", "read role")
    UPDATE = ("role:update", "update role")
    DELETE = ("role:delete", "delete role")


class PermissionPerm(DescribedEnum):
    FULL = ("permission:*", "full access to permissions")
    CREATE = ("permission:create", "create permission")
    READ = ("permission:read", "read permission")
    UPDATE = ("permission:update", "update permission")
    DELETE = ("permission:delete", "delete permission")


class RolePermissionPerm(DescribedEnum):
    FULL = ("role:permission:*", "full access to role permissions")
    ASSIGN = ("role:permission:assign", "assign permission to role")
    REVOKE = ("role:permission:revoke", "revoke permission from role")
    LIST = ("role:permission:list", "list role permissions")
