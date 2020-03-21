CODE_DIRS = api/ users/ works/ tests/
ISORT_PARAMS = --skip migrations/*
BLACK_PARAMS = --line-length 79

flake8:
	flake8 $(CODE_DIRS)

mypy:
	mypy $(CODE_DIRS)

isort:
	isort $(ISORT_PARAMS)

isort_travis_build:
	isort --check-only

black:
	black $(CODE_DIRS) $(BLACK_PARAMS)

black_travis_build:
	black $(CODE_DIRS) $(BLACK_PARAMS) --check