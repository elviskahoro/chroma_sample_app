from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from enum import Enum


def is_invalid_argument_exception(
    argument_type_str: str,
    argument_type_enum: Enum,
) -> Exception:
    error_msg: str = (
        f"Argument is not valid was not found for its argument type: {argument_type_str} :: {argument_type_enum}"
    )
    return ValueError(error_msg)


def is_valid_argument(
    argument_type_str: str,
    argument_type_enum: Enum,
) -> bool:
    return argument_type_enum.check_argument(
        argument=argument_type_str,
    )
