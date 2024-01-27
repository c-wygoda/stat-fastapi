from stat_fastapi.models.shared import Link


def find_link(links: list[Link], rel: str) -> Link | None:
    return next((link for link in links if link.rel == rel), None)
