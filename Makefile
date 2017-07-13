
init:
	pip install -u pip-tools
	pip-sync requirements/dev.txt

dev-reqs:
	pip-compile --output-file requirements/dev.txt requirements/prod.in requirements/dev.in

reqs:
	pip-compile --output-file requirements/prod.txt requirements/prod.in

test: clean flake
	pytest -v

flake:
	flake8

clean:
	find . -name '*.pyc' -delete
	find . -name '__pycache__' -type d -delete
