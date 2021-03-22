# OK Scoring Py

Repository for python backend for OK Scoring
Building in progress while reading through <https://www.cosmicpython.com/book/chapter_02_repository.html>
trying to apply concepts as much as possible as I go.

## Database set up

postgres docker container

create a file called `docker-compose.env` in the root directory of the repo

add the following env variables to set up your database with whatever values you want

```bash
POSTGRES_PASSWORD={some password}
POSTGRES_USER={some username}
POSTGRES_DB={db name}
```

use docker compose to build the volume, images and containers needed to run and connect to the database
`docker-compose up -d`

nav to <http://localhost:8080> to access the database.

### pytest



