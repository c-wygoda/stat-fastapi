from fastapi import Request
from pydantic import ValidationError

from stat_fastapi.backend.exceptions import ConstraintsException
from stat_fastapi.models.opportunity import (
    Opportunity,
    OpportunitySearch,
)
from stat_fastapi.models.product import Product, Provider, ProviderRole

from .models import Constraints, Pass, ValidatedOpportunitySearch
from .satellite import EarthObservationSatelliteModel
from .settings import Settings

PRODUCTS = [
    Product(
        id="mock:standard",
        description="Mock backend's standard product",
        license="CC0-1.0",
        providers=[
            Provider(
                name="ACME",
                roles=[
                    ProviderRole.licensor,
                    ProviderRole.producer,
                    ProviderRole.processor,
                    ProviderRole.host,
                ],
                url="http://acme.example.com",
            )
        ],
        constraints=Constraints.model_json_schema(),
        links=[],
    )
]


class StatMockBackend:
    satellites: list[EarthObservationSatelliteModel]

    def __init__(self):
        settings = Settings()
        self.satellites = [
            EarthObservationSatelliteModel(sat) for sat in settings.satellites
        ]

    async def products(self, request: Request) -> list[Product]:
        """
        Return a list of supported products.
        """
        return PRODUCTS

    async def product(self, product_id: str, request: Request) -> Product | None:
        """
        Return the product identified by `product_id` or `None` if it isn't
        supported.
        """
        return next(
            (
                product.model_copy(deep=True)
                for product in PRODUCTS
                if product.id == product_id
            ),
            None,
        )

    async def search_opportunities(
        self, search: OpportunitySearch, request: Request
    ) -> list[Opportunity]:
        """
        Search for ordering opportunities for the  given search parameters.
        """
        # Additional constraints validation according to this backend's constraints
        try:
            validated = ValidatedOpportunitySearch(**search.model_dump(by_alias=True))
        except ValidationError as exc:
            raise ConstraintsException(exc.errors()) from exc

        try:
            alt = validated.geometry.coordinates[2]
        except IndexError:
            alt = 0
        passes: list[Pass] = []
        for sat in self.satellites:
            passes += sat.passes(
                start=validated.properties.datetime[0],
                end=validated.properties.datetime[1],
                lon=validated.geometry.coordinates[0],
                lat=validated.geometry.coordinates[1],
                alt=alt,
                off_nadir_range=(
                    validated.properties.off_nadir.minimum,
                    validated.properties.off_nadir.maximum,
                ),
            )

        opportunities = [
            Opportunity(
                geometry=p.geometry,
                constraints=search.properties,
                properties=p.properties.model_dump(by_alias=True),
            )
            for p in passes
        ]
        return opportunities
