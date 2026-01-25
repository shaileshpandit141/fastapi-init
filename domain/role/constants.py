from core.enums import DescribedEnum


class RoleType(DescribedEnum):
    ADMIN = ("admin", "administrator with full access.")
    USER = ("user", "regular user with limited access.")
