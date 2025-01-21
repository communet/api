# FastAPI + Kafka DDD chat Application w\ MongoDB

The application for communication between users

## Requirements

- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)
- [GNU Make](https://www.gnu.org/software/make/)

## How to Use

1. **Clone the repository:**

   ```bash
   git clone git@github.com:communet/api.git
   cd api
   ```

2. Install all required packages in `Requirements` section.


### Implemented Commands

* `make app` - up application and infrastructure
* `make app-down` - down application and infrastructure
* `make app-exec` - go to contenerized interactive shell (bash)
* `make app-logs` - follow the logs in app container
* `make test` - run tests
* `make logs` - follow the logs in all containers
* `make pg-logs` - follow the logs in postgres container
* `make makemigrations` - generate new migration
* `make migrate` - apply all migrations
