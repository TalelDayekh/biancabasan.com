CODE_DIRS = works/
BLACK_PARAMS = --line-length 79

lint:
	flake8 $(CODE_DIRS)

annotation:
	mypy $(CODE_DIRS)

format:
	isort
	black $(CODE_DIRS)