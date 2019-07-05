CODE_DIRS = works/

lint:
	flake8 $(CODE_DIRS)

annotation:
	mypy $(CODE_DIRS)

format:
	isort
	black $(CODE_DIRS)