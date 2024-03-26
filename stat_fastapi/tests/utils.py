TYPE_JSON = "application/json"
TYPE_GEOJSON = "application/geo+json"


def find_link(links: list[dict], rel: str) -> dict | None:
    return next((link for link in links if link["rel"] == rel), None)
