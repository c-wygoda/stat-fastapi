from datetime import datetime, timedelta

from geojson_pydantic import Feature, Point
from pydantic import BaseModel, Field, field_validator, model_validator

from stat_fastapi.models.opportunity import (
    OpportunitySearch,
    OpportunitySearchProperties,
)
from stat_fastapi.models.order import OrderPayload, OrderPayloadProperties


class Satellite(BaseModel):
    tle: str
    block_time: tuple[timedelta, timedelta]

    @field_validator("tle")
    @classmethod
    def validate_tle(cls, v: str) -> str:
        lines = [line for line in v.split("\n") if line.strip() != ""]

        if len(lines) != 3:
            raise ValueError("TLE must be 3 lines")

        return v

    @property
    def tle_lines(self) -> tuple[str, str, str]:
        return self.tle.split("\n")


class PassProperties(BaseModel):
    datetime: datetime
    start: datetime
    end: datetime
    view_off_nadir: float = Field(..., alias="view:off_nadir")
    view_azimuth: float = Field(..., alias="view:azimuth")
    view_elevation: float = Field(..., alias="view:elevation")
    sun_elevation: float = Field(..., alias="sun:elevation")
    sun_azimuth: float = Field(..., alias="sun:azimuth")


class Pass(Feature[Point, PassProperties]):
    pass


OFF_NADIR_RANGE = (0.0, 45.0)
OFF_NADIR_DEFAULT_RANGE = (0.0, 30.0)
OFF_NADIR_MIN_SPREAD = 5.0


class OffNadirRange(BaseModel):
    minimum: float = Field(ge=OFF_NADIR_RANGE[0], le=OFF_NADIR_RANGE[1])
    maximum: float = Field(ge=OFF_NADIR_RANGE[0], le=OFF_NADIR_RANGE[1])

    @model_validator(mode="after")
    def validate(self) -> "OffNadirRange":
        diff = self.maximum - self.minimum
        if diff < OFF_NADIR_MIN_SPREAD:
            raise ValueError(f"range must be at least {OFF_NADIR_MIN_SPREAD}°")
        return self


class OpportunityConstraints(OpportunitySearchProperties):
    off_nadir: OffNadirRange = OffNadirRange(
        minimum=OFF_NADIR_DEFAULT_RANGE[0],
        maximum=OFF_NADIR_DEFAULT_RANGE[1],
    )


class ValidatedOpportunitySearch(OpportunitySearch):
    properties: OpportunityConstraints


class ValidatedOrderPayloadProperties(OrderPayloadProperties):
    off_nadir: OffNadirRange = OffNadirRange(
        minimum=OFF_NADIR_DEFAULT_RANGE[0],
        maximum=OFF_NADIR_DEFAULT_RANGE[1],
    )


class ValidatedOrderPayload(OrderPayload):
    properties: ValidatedOrderPayloadProperties
