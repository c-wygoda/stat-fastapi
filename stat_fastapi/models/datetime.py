from datetime import datetime
from typing import Annotated, Any, TypeAliasType

from pydantic import BeforeValidator, PlainSerializer, WithJsonSchema

# TODO: This is very much happy path...


def validate(val: Any) -> tuple[datetime, datetime]:
    if not isinstance(val, str):
        raise ValueError("not a valid datetime interval string")

    start, end = val.split("/", 1)

    start = datetime.fromisoformat(start)
    if start.tzinfo is None:
        raise ValueError("start datetime must have timezone info")

    end = datetime.fromisoformat(end)
    if start.tzinfo is None:
        raise ValueError("end datetime must have timezone info")

    return (start, end)


def serialize(value: tuple[datetime, datetime]) -> str:
    return f"{value[0].isoformat()}/{value[1].isoformat()}"


DatetimeInterval = TypeAliasType(
    "DatetimeInterval",
    Annotated[
        tuple[datetime, datetime],
        BeforeValidator(validate),
        PlainSerializer(serialize, return_type=str),
        WithJsonSchema({"type": "string"}, mode="serialization"),
    ],
)
