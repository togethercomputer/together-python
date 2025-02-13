.PHONY: all format lint test tests test_watch integration_tests docker_tests help extended_tests generate-client

# Default target executed when no arguments are given to make.
all: help

# Define a variable for the test file path.
TEST_FILE ?= tests/unit/

test:
	poetry run pytest $(TEST_FILE)

tests:
	poetry run pytest $(TEST_FILE)

test_watch:
	poetry run ptw --ignore ./tests/integration . -- ./tests/unit

extended_tests:
	poetry run pytest --only-extended ./tests/unit

integration_tests:
	poetry run pytest tests/integration


# Linting & Formatting

install:
	poetry install --with quality,tests
	poetry run pre-commit install
	$(MAKE) generate-client

format:
	poetry run pre-commit run --all-files

# OpenAPI Client Generation

generate-client:
	python scripts/generate_api_client.py

generate-client-from-existing-spec:
	python scripts/generate_api_client.py --skip-spec-download

# Documentation

html:
	make.bat html

help:
	@echo '===================='
	@echo '-- DOCUMENTATION ---'
	@echo '--------------------'
	@echo 'install                      - install dependencies'
	@echo 'format                       - run code formatters'
	@echo 'test                         - run unit tests'
	@echo 'tests                        - run unit tests'
	@echo 'test TEST_FILE=<test_file>   - run all tests in file'
	@echo 'test_watch                   - run unit tests in watch mode'
	@echo 'extended_tests               - run extended tests'
	@echo 'integration_tests            - run integration tests'
	@echo 'generate-client              - generate the OpenAPI client'
