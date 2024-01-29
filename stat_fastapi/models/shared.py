from typing import Optional

from geojson_pydantic import (
    GeometryCollection,
    LineString,
    MultiLineString,
    MultiPoint,
    MultiPolygon,
    Point,
    Polygon,
)
from pydantic import AnyUrl, BaseModel

Geometry = (
    Point
    | MultiPoint
    | LineString
    | MultiLineString
    | Polygon
    | MultiPolygon
    | GeometryCollection
)


class Link(BaseModel):
    href: AnyUrl
    rel: str
    type: Optional[str] = None
    title: Optional[str] = None


class HTTPException(BaseModel):
    detail: str
