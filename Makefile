APPLICATION_NAME = app
CODE = $(APPLICATION_NAME) tests

lint:  ##@Code Check code with pylint
	poetry run python3 -m pylint $(CODE)

format:  ##@Code Reformat code with isort and black
	poetry run python3 -m isort $(CODE)
	poetry run python3 -m black $(CODE)