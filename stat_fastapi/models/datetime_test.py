from datetime import UTC, datetime, timedelta

from pydantic import BaseModel

from .datetime import DatetimeInterval


class Model(BaseModel):
    datetime: DatetimeInterval


def test_deserialization():
    start = datetime.now(UTC)
    end = start + timedelta(hours=1)
    value = f"{start.isoformat()}/{end.isoformat()}"

    model = Model.model_validate_json(f'{{"datetime":"{value}"}}')

    assert model.datetime == (start, end)
