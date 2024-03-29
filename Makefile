PROJECT = uri
USE = development

.PHONY: all develop clean veryclean test watch release

all: clean develop test

develop: ${PROJECT}.egg-info/PKG-INFO

clean:
	find . -name __pycache__ -exec rm -rfv {} +
	find . -iname \*.pyc -exec rm -fv {} +
	find . -iname \*.pyo -exec rm -fv {} +
	rm -rvf build htmlcov

veryclean: clean
	rm -rvf *.egg-info .packaging/*

test: develop
	@clear
	@pytest --no-header --no-summary

watch: develop
	@clear
	@find . -iname \*.py | entr -c pytest --no-header --ff --maxfail=1

mpy: develop
	@clear
	@find uri -iname \*.py | entr -c mypy -p uri

release:
	@echo "Needs to be reimplemented."
	#./setup.py sdist bdist_wheel upload ${RELEASE_OPTIONS}
	#@echo -e "\nView online at: https://pypi.python.org/pypi/${PROJECT} or https://pypi.org/project/${PROJECT}/"
	#@echo -e "Remember to make a release announcement and upload contents of .packaging/release/ folder as a Release on GitHub.\n"

${PROJECT}.egg-info/PKG-INFO: pyproject.toml
	@mkdir -p ${VIRTUAL_ENV}/lib/pip-cache
	pip install --cache-dir "${VIRTUAL_ENV}/lib/pip-cache" -Ue ".[${USE}]"

