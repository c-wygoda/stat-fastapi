from datetime import datetime
from typing import Annotated, Any, Callable, TypeAliasType

from pydantic import (
    AfterValidator,
    AwareDatetime,
    BeforeValidator,
    WithJsonSchema,
    WrapSerializer,
)


def validate_before(value: Any):
    if isinstance(value, str):
        start, end = value.split("/", 1)
        return (start, end)
    return value


def validate_after(value: tuple[datetime, datetime]):
    if value[1] < value[0]:
        raise ValueError("end before start")
    return value


def serialize(
    value: tuple[datetime, datetime],
    serializer: Callable[[tuple[datetime, datetime]], tuple[str, str]],
) -> str:
    serialized = serializer(value)
    return f"{serialized[0]}/{serialized[1]}"


DatetimeInterval = TypeAliasType(
    "DatetimeInterval",
    Annotated[
        tuple[AwareDatetime, AwareDatetime],
        BeforeValidator(validate_before),
        AfterValidator(validate_after),
        WrapSerializer(serialize, return_type=str),
        WithJsonSchema({"type": "string"}, mode="serialization"),
    ],
)
