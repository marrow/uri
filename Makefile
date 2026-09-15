.PHONY: all develop clean veryclean install test watch format lint build release help

all: clean develop test  ## Default target: clean, install for local use, and execute tests.

develop: uri.egg-info/PKG-INFO  ## Install locally, in-place editable.

clean:  ## Delete all reproducible files.
	find . -name __pycache__ -exec rm -rfv {} +
	find . -iname \*.pyc -exec rm -fv {} +
	find . -iname \*.pyo -exec rm -fv {} +
	rm -rvf htmlcov

veryclean: clean  ## Also remove built packages and metadata.
	rm -rvf build *.egg-info .packaging/* "${VIRTUAL_ENV}/lib/pip-cache"

install:  ## Install project and dependencies in the local virtual environment.
	@mkdir -p ${VIRTUAL_ENV}/lib/pip-cache
	pip3 install --cache-dir "${VIRTUAL_ENV}/lib/pip-cache" -U .

watch: develop  ## Execute the test suite and linter on each detected file change.
	@clear
	@find . -iname \*.py | entr -c make lint format test

lint:  ## Perform project linting on each detected file change.
	@flake8 uri --toml-config pyproject.toml  # Deprecated due to upstream shenanigans re: pyproject.toml
	@mypy -p uri

format:  ## Format code with black and isort.
	black uri/
	isort uri/

test: develop  ## Execute the full test suite.
	@clear
	pytest --no-header --no-summary --ff

build:  ## Build a source and wheel distribution.
	python3 -m build

release: lint format test build  ## Build a source and wheel distribution.
	python3 -m pip install -U twine

	# twine upload --repository testpypi dist/*
	twine upload dist/*

	[[ `uname -s` == "Darwin" ]] && open dist

	@echo -e "\nView online at: https://pypi.python.org/pypi/uri or https://pypi.org/project/uri/"
	@echo -e "Remember to make a release announcement and upload contents of .packaging/release/ folder as a Release on GitHub.\n"

help:  ## Show this help message and exit.
	@echo "Usage: make <command>\n\033[36m\033[0m"
	@awk 'BEGIN {FS = ":.*##"} /^[a-zA-Z_-]+:.*?##/ { printf "\033[36m%-12s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST) | sort

uri.egg-info/PKG-INFO: pyproject.toml
	@mkdir -p ${VIRTUAL_ENV}/lib/pip-cache
	pip install --cache-dir "${VIRTUAL_ENV}/lib/pip-cache" -Ue ".[development]"
