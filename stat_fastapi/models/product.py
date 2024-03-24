from enum import Enum
from typing import Literal, Optional, Type

from pydantic import AnyHttpUrl, AnyUrl, BaseModel, field_serializer, field_validator

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


class Product(BaseModel):
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
    constraints: Optional[Type[BaseModel]] = None
    parameters: Optional[Type[BaseModel]] = None

    @field_serializer("constraints", "parameters")
    def serialize_model_schemas(self, attribute: Type[BaseModel] | None):
        # TODO: $defs paths are off in resulting JSON
        if attribute is not None:
            return attribute.model_json_schema()

    @field_validator("constraints", "parameters")
    @classmethod
    def unset_model_schemas(cls, _) -> None:
        # really only for tests, but ignore the JSON schema fields
        return None


class ProductsCollection(BaseModel):
    type: Literal["ProductCollection"] = "ProductCollection"
    products: list[Product]
