all:
	python3 test.py

t: test
test:
	python -m pytest *.py --ignore=venv -vv --doctest-module
