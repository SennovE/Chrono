APPLICATION_NAME = app
CODE = $(APPLICATION_NAME) tests

lint:  ##@Code Check code with pylint
	poetry run python3 -m pylint $(CODE)

format:  ##@Code Reformat code with isort and black
	poetry run python3 -m isort $(CODE)
	poetry run python3 -m black $(CODE)

db:  ##@Database Create database with docker-compose
	docker-compose -f docker-compose.yml up -d --remove-orphans

migrate:  ##@Migrate database
	cd db && alembic upgrade head