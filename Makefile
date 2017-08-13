
init:
	pip install -U pip-tools
	pip-sync requirements/dev.txt

reqs:
	pip-compile -U -o requirements/prod.txt requirements/prod.in
	pip-compile -U -o requirements/dev.txt requirements/prod.in requirements/dev.in
	pip-sync requirements/dev.txt

test: clean flake
	pytest -v

coverage: clean flake
	py.test --cov-report term-missing:skip-covered --cov=.

flake:
	flake8

clean:
	find . -regex '*.py(c|o)' -delete
	find . -name '__pycache__' -type d -delete
