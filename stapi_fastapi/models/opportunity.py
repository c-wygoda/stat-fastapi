from typing import Literal, Optional

from geojson_pydantic import Feature, FeatureCollection
from geojson_pydantic.geometries import Geometry
from pydantic import BaseModel, ConfigDict

from stapi_fastapi.types.datetime_interval import DatetimeInterval
from stapi_fastapi.types.filter import CQL2Filter


# Copied and modified from stack_pydantic.item.ItemProperties
class OpportunityProperties(BaseModel):
    datetime: DatetimeInterval
    product_id: str
    model_config = ConfigDict(extra="allow")


class OpportunityRequest(OpportunityProperties):
    geometry: Geometry
    filter: Optional[CQL2Filter] = None


class Opportunity(Feature[Geometry, OpportunityProperties]):
    type: Literal["Feature"] = "Feature"


class OpportunityCollection(FeatureCollection[Opportunity]):
    type: Literal["FeatureCollection"] = "FeatureCollection"
