from typing import Any, Literal, Mapping

from geojson_pydantic import Feature, FeatureCollection
from pydantic import BaseModel, ConfigDict

from .datetime import DatetimeInterval
from .shared import Geometry


class OpportunitySearchProperties(BaseModel):
    datetime: DatetimeInterval

    model_config = ConfigDict(extra="allow")


OpportunityProperties = Mapping[str, Any]


class OpportunitySearch(Feature[Geometry, OpportunitySearchProperties]):
    product_id: str


class Opportunity(Feature[Geometry, OpportunityProperties]):
    type: Literal["Feature"] = "Feature"
    constraints: OpportunitySearchProperties


class OpportunityCollection(FeatureCollection[Opportunity]):
    type: Literal["FeatureCollection"] = "FeatureCollection"
