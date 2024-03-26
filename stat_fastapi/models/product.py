from enum import Enum
from typing import Generic, Literal, Optional, TypeVar

from geojson_pydantic import Feature
from geojson_pydantic.geometries import Geometry
from pydantic import (
    AnyHttpUrl,
    AnyUrl,
    BaseModel,
    computed_field,
)

# shouldn't use this, but I'm lazy
# see https://github.com/pydantic/pydantic/issues/4908#issuecomment-1538769435
from pydantic._internal._generics import get_args

from stat_fastapi.consts import STAT_VERSION

from .shared import Link


class ProviderRole(str, Enum):
    licensor = "licensor"
    producer = "producer"
    processor = "processor"
    host = "host"


class Provider(BaseModel):
    name: str
    description: Optional[str] = None
    roles: list[ProviderRole]
    url: AnyHttpUrl


Constraints = TypeVar("Constraints", bound=None | BaseModel)
Geom = TypeVar("Geom", bound=Geometry)


class Product(BaseModel, Generic[Geom, Constraints]):
    type: Literal["Product"] = "Product"
    stat_version: str = STAT_VERSION
    stat_extensions: Optional[list[AnyUrl]] = None
    id: str
    title: Optional[str] = None
    description: str
    keywords: Optional[list[str]] = None
    license: str
    providers: list[Provider]
    links: list[Link]

    @computed_field
    @property
    def constraints(self) -> dict | None:
        constraints: BaseModel | None = get_args(self)[0]
        if constraints is not None:
            return constraints.model_json_schema()

    # TODO: parameters. merging models ain't fun

    @property
    def OrderPayload(self):
        args = get_args(self)
        geom: Geometry = args[0]
        constraints: BaseModel | None = args[1]

        class OrderPayload(Feature[geom, constraints]):
            product_id: str = self.id

        return OrderPayload


class ProductsCollection(BaseModel):
    type: Literal["ProductCollection"] = "ProductCollection"
    products: list[Product]
