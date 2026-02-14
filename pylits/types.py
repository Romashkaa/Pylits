from typing import Any, TypeAlias

SupportedTypes: TypeAlias = bool | int | float | str | list["SupportedTypes"] | tuple["SupportedTypes", ...] | set["SupportedTypes"] | dict["SupportedTypes", "SupportedTypes"] | None

__all__ = ["SupportedTypes"]