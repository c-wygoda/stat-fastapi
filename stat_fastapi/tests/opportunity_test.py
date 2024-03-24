from datetime import UTC, datetime, timedelta
from typing import Generator

from fastapi import status
from fastapi.testclient import TestClient
from httpx import Response
from pytest import fixture

from stat_fastapi.models.opportunity import OpportunityCollection

from .utils import TYPE_GEOJSON

NOW = datetime.now(UTC)
START = NOW
END = START + timedelta(days=5)


@fixture(scope="module")
def search_opportunities_response(
    stat_client: TestClient, product_id: str
) -> Generator[Response, None, None]:
    res = stat_client.post(
        "/opportunities",
        json={
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [0, 0],
            },
            "product_id": product_id,
            "properties": {
                "datetime": f"{START.isoformat()}/{END.isoformat()}",
                "off_nadir": {
                    "minimum": 0,
                    "maximum": 45,
                },
            },
        },
    )
    assert res.status_code == status.HTTP_200_OK
    assert res.headers["Content-Type"] == TYPE_GEOJSON
    yield res


def test_search_opportunities_response(
    search_opportunities_response: Response,
):
    response = OpportunityCollection(**search_opportunities_response.json())
    assert len(response.features) > 0
