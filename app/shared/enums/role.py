from ._base import LabeledEnum

# =============================================================================
# Role Enum.
# =============================================================================


class RoleEnum(LabeledEnum):
    SUPERADMIN = ("superadmin", "Unrestricted access and control.")
    ADMIN = ("admin", "Administrator with elevated access.")
    USER = ("user", "Regular user with limited access.")
