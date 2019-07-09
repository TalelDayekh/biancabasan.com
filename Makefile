CODE_DIRS = src/backend/api src/backend/users src/backend/works/
BLACK_PARAMS = --line-length 79

lint:
	flake8 $(CODE_DIRS)

annotation:
	mypy $(CODE_DIRS)

format:
	isort
	black $(CODE_DIRS)