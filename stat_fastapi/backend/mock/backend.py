from fastapi import Request
from pydantic import ValidationError

from stat_fastapi.backend.exceptions import ConstraintsException, NotFoundException
from stat_fastapi.models.opportunity import (
    Opportunity,
    OpportunitySearch,
)
from stat_fastapi.models.order import Order, OrderPayload
from stat_fastapi.models.product import Product, Provider, ProviderRole

from .models import (
    OpportunityConstraints,
    Pass,
    ValidatedOpportunitySearch,
    ValidatedOrderPayload,
    ValidatedOrderPayloadProperties,
)
from .repository import Repository
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
        constraints=OpportunityConstraints,
        properties=ValidatedOrderPayloadProperties,
        links=[],
    )
]


class StatMockBackend:
    satellites: list[EarthObservationSatelliteModel]
    repository: Repository

    def __init__(self):
        settings = Settings.load()
        self.satellites = [
            EarthObservationSatelliteModel(sat) for sat in settings.satellites
        ]
        self.repository = Repository(settings.database)

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
        try:
            return next(
                (
                    product.model_copy(deep=True)
                    for product in PRODUCTS
                    if product.id == product_id
                ),
            )
        except StopIteration as exc:
            raise NotFoundException() from exc

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

    async def create_order(self, payload: OrderPayload, request: Request) -> Order:
        """
        Create a new order.
        """
        try:
            validated = ValidatedOrderPayload(**payload.model_dump(by_alias=True))
        except ValidationError as exc:
            raise ConstraintsException(exc.errors()) from exc

        return await self.repository.create(validated)

    async def get_order(self, order_id: str, request: Request):
        """
        Show details for order with `order_id`.
        """
        feature = await self.repository.get(order_id)
        if feature is None:
            raise NotFoundException()
        return feature
