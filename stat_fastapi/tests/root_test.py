from warnings import warn

from fastapi import status
from fastapi.testclient import TestClient
from pytest import fixture

from stat_fastapi.models.root import RootResponse

from .utils import find_link
from .warnings import StatSpecWarning


@fixture(scope="module")
def data(stat_client: TestClient):
    res = stat_client.get("/")

    assert res.status_code == status.HTTP_200_OK
    assert res.headers["Content-Type"] == "application/json"

    yield RootResponse(**res.json())


def test_root_self_link(data: RootResponse, url_for):
    link = find_link(data.links, "self")
    if link is None:
        warn(StatSpecWarning("GET / Link[rel=self] should exist"))
    else:
        assert link.type == "application/json"
        assert link.href == url_for("/")


def test_root_service_description_link(data: RootResponse, base_url: str):
    link = find_link(data.links, "service-description")
    if link is None:
        warn(StatSpecWarning("GET / Link[rel=service-description] should exist"))

    else:
        assert link.type == "application/json"
        assert str(link.href) == f"{base_url.rstrip('/')}/openapi.json"


def test_root_service_docs_link(data: RootResponse, base_url: str):
    link = find_link(data.links, "service-docs")
    if link is None:
        warn(StatSpecWarning("GET / Link[rel=service-docs] should exist"))
    else:
        assert link.type == "text/html"
        assert str(link.href) == f"{base_url.rstrip('/')}/docs"
