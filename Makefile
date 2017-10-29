.PHONY: init lint test

init:
	python initialise_db.py

lint:
	mypy dpflask
	mypy tests --ignore-missing-imports
	flake8 dpflask
	flake8 tests

test:
	pytest tests