from datetime import UTC, datetime, timedelta
from typing import Generator

from fastapi import status
from fastapi.testclient import TestClient
from httpx import Response
from pytest import fixture

from stat_fastapi.models.order import Order, OrderStatus
from stat_fastapi.tests.utils import TYPE_GEOJSON

NOW = datetime.now(UTC)
START = NOW
END = START + timedelta(days=5)


@fixture(scope="module")
def new_order_response(
    stat_client: TestClient, product_id: str
) -> Generator[Response, None, None]:
    res = stat_client.post(
        "/orders",
        json={
            "product_id": product_id,
            "geometry": {"type": "Point", "coordinates": [0, 0]},
            "properties": {"datetime": f"{START.isoformat()}/{END.isoformat()}"},
        },
    )

    assert res.status_code == status.HTTP_201_CREATED
    assert res.headers["Content-Type"] == TYPE_GEOJSON
    yield res


def test_new_order_location_header_matches_self_link(new_order_response: Response):
    order = Order(**new_order_response.json())
    assert new_order_response.headers["Location"] == next(
        (str(link.href) for link in order.links if link.rel == "self")
    )


def test_new_order_status_is_pending(new_order_response: Response):
    order = Order(**new_order_response.json())
    assert order.properties.status == OrderStatus.pending
    assert order.properties.off_nadir == {"minimum": 0, "maximum": 30}


@fixture(scope="module")
def get_order_response(
    stat_client: TestClient, new_order_response: Response
) -> Generator[Response, None, None]:
    order_id = Order(**new_order_response.json()).id

    res = stat_client.get(f"/orders/{order_id}")

    assert res.status_code == status.HTTP_200_OK
    assert res.headers["Content-Type"] == TYPE_GEOJSON
    yield res


def test_get_order_properties(get_order_response: Response):
    order = Order(**get_order_response.json())

    assert order.geometry.model_dump(exclude_unset=True) == {
        "type": "Point",
        "coordinates": (0, 0),
    }

    assert order.properties.datetime == (START, END)
    assert order.properties.status == OrderStatus.pending
    assert order.properties.off_nadir == {"minimum": 0, "maximum": 30}
