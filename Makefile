CODE_DIRS = src/backend/api/ src/backend/users/ src/backend/works/
BLACK_PARAMS = --line-length 79

flake8:
	flake8 $(CODE_DIRS)

mypy:
	mypy $(CODE_DIRS)

isort:
	isort

isort_travis_build:
	isort --check-only

black:
	black $(CODE_DIRS) $(BLACK_PARAMS)

black_travis_build:
	black $(CODE_DIRS) $(BLACK_PARAMS) --check