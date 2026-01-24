from typing import Any
from pydantic import field_validator
from uuid import UUID


def validate_uuid(value: Any) -> UUID:
    if isinstance(value, str):
        try:
            return UUID(value)
        except ValueError:
            raise ValueError("Invalid UUID format")
    if isinstance(value, UUID):
        return value
    raise ValueError("Value must be a valid UUID")


def validate_string_length(value: str, min_length: int = 1, max_length: int = None) -> str:
    if not isinstance(value, str):
        raise ValueError("Value must be a string")
    if len(value.strip()) < min_length:
        raise ValueError(f"String must be at least {min_length} characters long")
    if max_length and len(value) > max_length:
        raise ValueError(f"String must be at most {max_length} characters long")
    return value.strip()


def validate_positive_integer(value: int, min_value: int = 1) -> int:
    if not isinstance(value, int):
        raise ValueError("Value must be an integer")
    if value < min_value:
        raise ValueError(f"Value must be at least {min_value}")
    return value


def validate_range(value: float, min_value: float = None, max_value: float = None) -> float:
    if not isinstance(value, (int, float)):
        raise ValueError("Value must be a number")
    if min_value is not None and value < min_value:
        raise ValueError(f"Value must be at least {min_value}")
    if max_value is not None and value > max_value:
        raise ValueError(f"Value must be at most {max_value}")
    return float(value)


def validate_email(value: str) -> str:
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, value):
        raise ValueError("Invalid email format")
    return value


def validate_url(value: str) -> str:
    import re
    pattern = r'^https?://(?:[-\w.])+(?:[:\d]+)?(?:/(?:[\w/_.])*(?:\?(?:[\w&=%.])*)?(?:#(?:\w)*)?)?$'
    if not re.match(pattern, value):
        raise ValueError("Invalid URL format")
    return value


def validate_not_empty(value: Any) -> Any:
    if value is None:
        raise ValueError("Field cannot be empty")
    if isinstance(value, str) and not value.strip():
        raise ValueError("Field cannot be empty")
    if isinstance(value, (list, dict)) and len(value) == 0:
        raise ValueError("Field cannot be empty")
    return value
