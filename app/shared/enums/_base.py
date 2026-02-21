from enum import Enum

# =============================================================================
# Function to convert enum to list of vlaues.
# =============================================================================


def get_enum_values(enums: type[Enum]) -> list[str]:
    return [e.value for e in enums]


# =============================================================================
# Labeled enum for role and permissions.
# =============================================================================


class LabeledEnum(Enum):
    @property
    def value(self) -> str:
        return self._value_[0]

    @property
    def label(self) -> str:
        return self._value_[1]

    @classmethod
    def choices(cls) -> list[tuple[str, str]]:
        return [(item.value, item.label) for item in cls]
