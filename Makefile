PROJECT = uri
USE = development

.PHONY: all develop clean veryclean test watch release

all: clean develop test  ## Clean up, install for development use, and execute tests.

develop: ${PROJECT}.egg-info/PKG-INFO  ## Install locally, in-place editable.

clean:  ## Delete all reproducible files.
	find . -name __pycache__ -exec rm -rfv {} +
	find . -iname \*.pyc -exec rm -fv {} +
	find . -iname \*.pyo -exec rm -fv {} +
	rm -rvf build htmlcov

veryclean: clean  ## Also remove built packages and metadata.
	rm -rvf *.egg-info .packaging/*

test: develop  ## Execute the full test suite.
	@clear
	@pytest --no-header --no-summary

watch: develop  ## Execute the test suite on each detected file change.
	@clear
	@find . -iname \*.py | entr -c pytest --no-header --ff --maxfail=1

mpy: develop  ## Perform project linting on each detected file change.
	@clear
	@find uri -iname \*.py | entr -c mypy -p uri

build:  ## Minimal build automation.
	python3 -m build

release:  ## Build a source and wheel distribution.
	@echo "Needs to be reimplemented."
	
	python3 -m build --sdist --wheel
	[[ `uname -s` == "Darwin" ]] && open .packaging/release
	
	#./setup.py sdist bdist_wheel upload ${RELEASE_OPTIONS}
	#@echo -e "\nView online at: https://pypi.python.org/pypi/${PROJECT} or https://pypi.org/project/${PROJECT}/"
	#@echo -e "Remember to make a release announcement and upload contents of .packaging/release/ folder as a Release on GitHub.\n"

help:  ## Show this help message and exit.
	@echo "Usage: make <command>\n\033[36m\033[0m"
	@awk 'BEGIN {FS = ":.*##"} /^[a-zA-Z_-]+:.*?##/ { printf "\033[36m%-12s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST) | sort

${PROJECT}.egg-info/PKG-INFO: pyproject.toml
	@mkdir -p ${VIRTUAL_ENV}/lib/pip-cache
	pip install --cache-dir "${VIRTUAL_ENV}/lib/pip-cache" -Ue ".[${USE}]"

