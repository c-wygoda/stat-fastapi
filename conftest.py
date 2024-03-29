from pytest import Parser


def pytest_addoption(parser: Parser):
    parser.addoption(
        "--stat-backend",
        action="store",
        default="stat_fastapi.backend.mock:StatMockBackend",
    )
    parser.addoption("--stat-prefix", action="store", default="/stat")
    parser.addoption("--stat-product-id", action="store", default="mock:standard")
