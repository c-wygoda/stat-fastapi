# STAT FastAPI - Spatio Temporal Asset Tasking with FastAPI

WARNING: The whole STAT spec is very much work in progress, so things are
guaranteed to be not correct. One way or the other.

## Usage

STAT FastAPI provides an `fastapi.APIRouter` which must be included in
`fastapi.FastAPI` instance.

## Development

It's 2024 and we still need to pick our poison for a 2024 dependency management
solution. This project picks [poetry][poetry] for now.

### Dev Setup

Setup is managed with `poetry` and `pre-commit`, all of which can be initialised
by `make bootstrap`.

### Test Suite

A `pytest` based test suite is provided. Run it as `make test` or with
additional pytest options in `PYTEST_ADDOPTS`:

```
make PYTEST_ADDOPTS="-x --ff" test
```

A number of STAT specific pytest options are available through the test suite:

- `--stat-backend`: backend implementation to use in tests, defaults to
  `stat_fastapi.backend.mock:StatMockBackend`
- `--stat-prefix`: service URL prefix, defaults to `/prefix`
- `--stat-product-id`: STAT product id to use in tests, defaults to
  `mock:standard`

### Dev Server

For dev purposes, [stat_fastapi.**dev**.py](./stat_fastapi/__dev__.py) shows
a minimal demo with `uvicorn` to run the full app. Start it with `make dev`.

### Implementing a backend

- The test suite assumes the backend can be instantiated without any paramters
  required by the constructor.

[poetry]: https://python-poetry.org
