from typing import Generator
from warnings import warn

from fastapi import status
from fastapi.testclient import TestClient
from pytest import fixture

from .utils import TYPE_JSON, find_link
from .warnings import StatSpecWarning


@fixture(scope="module")
def data(stat_client: TestClient) -> Generator[dict, None, None]:
    res = stat_client.get("/")

    assert res.status_code == status.HTTP_200_OK
    assert res.headers["Content-Type"] == TYPE_JSON

    yield res.json()


def test_root_self_link(data, url_for):
    link = find_link(data["links"], "self")
    if link is None:
        warn(StatSpecWarning("GET / Link[rel=self] should exist"))
    else:
        assert link["type"] == TYPE_JSON
        assert link["href"] == str(url_for("/"))


def test_root_service_description_link(data, base_url: str):
    link = find_link(data["links"], "service-description")
    if link is None:
        warn(StatSpecWarning("GET / Link[rel=service-description] should exist"))

    else:
        assert link["type"] == TYPE_JSON
        assert link["href"] == f"{base_url.rstrip('/')}/openapi.json"


def test_root_service_docs_link(data, base_url: str):
    link = find_link(data["links"], "service-docs")
    if link is None:
        warn(StatSpecWarning("GET / Link[rel=service-docs] should exist"))
    else:
        assert link["type"] == "text/html"
        assert link["href"] == f"{base_url.rstrip('/')}/docs"
