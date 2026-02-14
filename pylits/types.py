from typing import Any, TypeAlias

SupportedHashableTypes: TypeAlias = bool | int | float | str | tuple["SupportedHashableTypes", ...] | None
SupportedTypes: TypeAlias = bool | int | float | str | list["SupportedTypes"] | tuple["SupportedTypes", ...] | set["SupportedTypes"] | dict[SupportedHashableTypes, "SupportedTypes"] | None

__all__ = ["SupportedTypes", "SupportedHashableTypes"]