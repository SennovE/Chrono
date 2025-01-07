
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

ALEMBIC_CMD = alembic
TARGET_DIR = backend/app/database
.PHONY: migration
ENV_FILE = .env
BACKUP_FILE = .env.bak
HOST_KEY = POSTGRES_HOST

set-localhost:
	@if grep -q "^$(HOST_KEY)=" $(ENV_FILE); then \
		cp $(ENV_FILE) $(BACKUP_FILE); \
		sed -i "s/^$(HOST_KEY)=.*/$(HOST_KEY)=localhost/" $(ENV_FILE); \
		echo "$(HOST_KEY) временно установлен в localhost"; \
	else \
		echo "$(HOST_KEY) не найден в $(ENV_FILE)"; \
		exit 1; \
	fi
reset-host:
	@if [ -f $(BACKUP_FILE) ]; then \
		mv $(BACKUP_FILE) $(ENV_FILE); \
		echo "$(HOST_KEY) восстановлен в исходное состояние"; \
	else \
		echo "Резервная копия $(BACKUP_FILE) не найдена. Восстановление невозможно."; \
		exit 1; \
	fi
# возможно надо поменть в database/models/alembic sqlalchemy.url = postgresql://%(POSTGRES_USER)s:%(POSTGRES_PASSWORD)s@localhost:%(POSTGRES_PORT)s/%(POSTGRES_DB)s?target_session_attrs=read-write
migration_auto:
	$(MAKE) set-localhost
	$(MAKE) run 
	@if [ -z "$(filter-out $@,$(MAKECMDGOALS))" ]; then \
		echo "Usage: make migration <migration_name>"; \
		$(MAKE) reset-host; \
		exit 1; \
	fi; \
	cd $(TARGET_DIR) && $(ALEMBIC_CMD) revision --autogenerate -m "$(filter-out $@,$(MAKECMDGOALS))"
	$(MAKE) reset-host
	$(MAKE) run 
migration:
	@if [ -z "$(filter-out $@,$(MAKECMDGOALS))" ]; then \
		echo "Usage: make mg <migration_message>"; \
		exit 1; \
	fi; \
	cd $(TARGET_DIR) && $(ALEMBIC_CMD) revision --autogenerate -m "$(filter-out $@,$(MAKECMDGOALS))"
upgrade:
	cd $(TARGET_DIR) && $(ALEMBIC_CMD) upgrade head
FRONT_DIR = frontend
run_front:
	cd $(FRONT_DIR) && npm run serve
poetry:
	cd backend && poetry install && poetry shell
reboot:
	cd .. && sudo rm -rf Chrono && git clone git@github.com:SennovE/Chrono.git && cd Chrono/backend && poetry install && poetry shell
	$(MAKE) env
	$(MAKE) run
	$(MAKE) run_front
.PHONY: new_br
new_br:
	@if [ -z "$(filter-out $@,$(MAKECMDGOALS))" ]; then \
		echo "need a name of the branch"; \
		exit 1; \
	fi; \
	branch_name="$(filter-out $@,$(MAKECMDGOALS))"; \
	git branch "$$branch_name" && git checkout "$$branch_name" && git branch
.PHONY: create-env

env:
	@echo "POSTGRES_DB=database" > .env
	@echo "POSTGRES_HOST=postgres" >> .env
	@echo "POSTGRES_USER=user" >> .env
	@echo "POSTGRES_PASSWORD=password" >> .env
	@echo "POSTGRES_PORT=5432" >> .env
	@echo "" >> .env
	@echo "BACKEND_HOST=backend" >> .env
	@echo "BACKEND_PORT=8080" >> .env
	@echo "PATH_PREFIX=/api/v1" >> .env
	@echo "" >> .env
	@echo "SECRET_KEY=123" >> .env
	@echo "ALGORITHM=HS256" >> .env
	@echo "ACCESS_TOKEN_EXPIRE_MINUTES=10080" >> .env