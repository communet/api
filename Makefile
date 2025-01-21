DC = docker compose
EXEC = docker exec -it
LOGS = docker logs
APP_CONTAINER = communet-api
POSTGRES_CONTAINER = communet-postgres

.PHONY: app
app:
	${DC} up --build -d

.PHONY: app-down
app-down:
	${DC} down

.PHONY: app-exec
app-exec:
	${EXEC} ${APP_CONTAINER} bash

.PHONY: app-logs
app-logs:
	${LOGS} ${APP_CONTAINER} -f

.PHONY: test
test:
	${EXEC} ${APP_CONTAINER} pytest

.PHONY: logs
logs:
	${DC} logs -f

.PHONY: pg-logs
pg-logs:
	${LOGS} ${POSTGRES_CONTAINER} -f

.PHONY: makemigrations
makemigrations:
	${EXEC} ${APP_CONTAINER} alembic revision --autogenerate

.PHONY: migrate
migrate:
	${EXEC} ${APP_CONTAINER} alembic upgrade head
