from enum import Enum


class LabeledEnum(Enum):
    @property
    def value(self) -> str:
        return self._value_[0]

    @property
    def description(self) -> str:
        return self._value_[1]

    @classmethod
    def choices(cls) -> list[tuple[str, str]]:
        return [(item.value, item.description) for item in cls]
