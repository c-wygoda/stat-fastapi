from enum import Enum
from typing import Literal

from geojson_pydantic import Feature
from pydantic import AwareDatetime, BaseModel, ConfigDict

from .datetime import DatetimeInterval
from .shared import Geometry, Link


class OrderPayloadProperties(BaseModel):
    datetime: DatetimeInterval

    model_config = ConfigDict(extra="allow")


class OrderPayload(Feature[Geometry, OrderPayloadProperties]):
    type: Literal["Feature"] = "Feature"
    product_id: str


class OrderStatus(str, Enum):
    pending = "pending"
    processing = "processing"
    finished = "finished"
    failed = "failed"
    expired = "expired"


class OrderProperties(BaseModel):
    datetime: DatetimeInterval
    status: OrderStatus
    created_at: AwareDatetime
    updated_at: AwareDatetime

    model_config = ConfigDict(extra="allow")


class Order(Feature[Geometry, OrderProperties]):
    type: Literal["Feature"] = "Feature"
    product_id: str
    links: list[Link]
