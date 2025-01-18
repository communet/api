DC = docker compose
EXEC = docker exec -it
LOGS = docker logs
APP_CONTAINER = backend

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