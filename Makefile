CODE_DIRS = src/backend/api src/backend/users src/backend/works/
ISORT_PARAMS = --check-only
BLACK_PARAMS = --line-length 79 --check

# format:
# 	isort $(ISORT_PARAMS)
# 	black $(CODE_DIRS) $(BLACK_PARAMS)

flake8:
	flake8 $(CODE_DIRS)

mypy:
	mypy $(CODE_DIRS)

isort:
	isort

black:
	black $(CODE_DIRS) --line-length 79