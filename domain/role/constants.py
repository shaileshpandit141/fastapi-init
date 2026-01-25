from core.enums import DescribedEnum


class RoleType(DescribedEnum):
    SUPERUSER = (
        "superuser",
        "system-level user with unrestricted access and control.",
    )
    ADMIN = ("admin", "administrator with full access.")
    USER = ("user", "regular user with limited access.")
