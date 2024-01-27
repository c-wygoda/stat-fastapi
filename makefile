SHELL = bash
.DEFAULT_GOAL := help

.PHONY: bootstrap
bootstrap: ## Bootstrap local repository checkout
	@echo Installing Python dependencies into Poetry managed virtualenv
ifeq (, $(shell which poetry))
	@echo "No \`poetry\` in \$$PATH, please install poetry https://python-poetry.org"
else
	poetry install --with dev
endif

	poetry run pre-commit install


export PYTEST_ADDOPTS=--cov=stat_fastapi
.PHONY: test
test: ## Run test suite
	poetry run pytest


.PHONY: dev
dev: ## Run dev server
	poetry run stat_fastapi/__dev__.py


.PHONY: help
help:
	@echo "Welcome to STAT FastAPI!"
	@echo
	@grep -E '^[\.a-zA-Z0-9_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
