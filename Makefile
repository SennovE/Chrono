
CODE = backend/app backend/tests

lint:  ##@Code Check code with pylint
	poetry run python3 -m pylint $(CODE)

format:  ##@Code Reformat code with isort and black
	poetry run python3 -m isort $(CODE)
	poetry run python3 -m black $(CODE)

run:  ##@Create database and run api with migrations
	docker-compose -f docker-compose.yml up -d --remove-orphans

docker_clear:  ##@Clear all docker files
	docker stop $$(docker ps -q)
	docker rm $$(docker ps -a -q)
	docker rmi $$(docker images -a -q)
	docker volume rm $$(docker volume ls -q)
	docker network prune -f
