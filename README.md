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

<http://localhost:5005> to access the app locally

### pytest

to run e2e/integration/unit tests run `pytest`

to run e2e tests only
```bash
pytest ./tests/e2e
```

to run an individual e2e test

```bash
pytest ./tests/e2e/test_play_cribbage_v2.py
```

### Alembic migrations

Create a migration:

`alembic revision --autogenerate -m "Some message"`

The trick is to make sure that the mapper code is run before the alembic config code is via imports
if this is not the case, then the auto migrations will not pick up the data from the mappers

then run the migration

`alembic upgrade head`

## Delete Data

```sql
delete from "gameRules";
delete from "gameRulesV2";
delete from "scoreRound";
delete from "playerScoreHistory";
delete from game;
delete from player;
```

## TODO List

List of items I would like to accomplish

- refactor e2e tests to use a base test function that can be passed scenarios to test []
- Performance testing to identify weak points []
- Security []
- Build the v2 API in fastify and performance test []
- Clean up existing service code and tests []
  - Rules service could really use some attention I think
- Add passing Yahtzee e2e test []
- CI/CD []
- Frontend app for managing game rules []
- Add endpoints for []
    - duplicating a game
    - deleting data?
- ML and analytics package []


