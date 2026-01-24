from enum import StrEnum


class Perm:
    class User(StrEnum):
        FULL = "user:*"
        CREATE = "user:create"
        READ = "user:read"
        UPDATE = "user:update"
        DELETE = "user:delete"

    class UserRole(StrEnum):
        FULL = "user:role:*"
        ASSIGN = "user:role:assign"
        REVOKE = "user:role:revoke"
        LIST = "user:role:list"
