
init:
	pip install -U pip-tools
	pip-sync requirements/dev.txt

dev-reqs:
	pip-compile --output-file requirements/dev.txt requirements/prod.in requirements/dev.in

reqs:
	pip-compile --output-file requirements/prod.txt requirements/prod.in

test: clean flake
	pytest -v

coverage: clean flake
	py.test --cov-report term-missing:skip-covered --cov=.

flake:
	flake8

clean:
	find . -regex '*.py(c|o)' -delete
	find . -name '__pycache__' -type d -delete
