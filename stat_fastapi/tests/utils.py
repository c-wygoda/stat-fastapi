from stat_fastapi.models.shared import Link

TYPE_JSON = "application/json"
TYPE_GEOJSON = "application/geo+json"


def find_link(links: list[Link], rel: str) -> Link | None:
    return next((link for link in links if link.rel == rel), None)
