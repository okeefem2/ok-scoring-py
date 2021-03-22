# pylint: disable=redefined-outer-name
import time
from dataclasses import asdict
from pathlib import Path

import pytest
import requests
from requests.exceptions import ConnectionError
from sqlalchemy.exc import OperationalError
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers


@pytest.fixture
def in_memory_db():
    engine = create_engine("sqlite:///:memory:")
    metadata.create_all(engine)
    return engine


@pytest.fixture
def session(in_memory_db):
    start_mappers()
    yield sessionmaker(bind=in_memory_db)()
    clear_mappers()


def wait_for_postgres_to_come_up(engine):
    deadline = time.time() + 10
    while time.time() < deadline:
        try:
            return engine.connect()
        except OperationalError:
            time.sleep(0.5)
    pytest.fail("Postgres never came up")


def wait_for_webapp_to_come_up():
    deadline = time.time() + 10
    url = ok_scoring_config.get_api_url()
    while time.time() < deadline:
        try:
            return requests.get(url)
        except ConnectionError:
            time.sleep(0.5)
    pytest.fail("API never came up")


@pytest.fixture(scope="session")
def postgres_db():
    engine = create_engine(ok_scoring_config.get_postgres_uri())
    wait_for_postgres_to_come_up(engine)
    metadata.create_all(engine)
    return engine


@pytest.fixture
def postgres_session(postgres_db):
    start_mappers()
    yield sessionmaker(bind=postgres_db)()
    clear_mappers()


@pytest.fixture
def add_game(postgres_session):
    games_added = set()
    players_added = set()

    # For each player, create a score history
    def _add_game(game: Game, players: [str], rules: GameRules = None):
        game_num = len(games_added) + 1
        postgres_session.execute(
            "INSERT INTO game (key, description, date)"
            " VALUES (:key, :description, :date)",
            dict(key=game.key, description=game.description, date=game.date),
        )
        games_added.add(game_key)

        if rules is not None:
            rules.gameKey = game_key
            # TODO all props
            postgres_session.execute(
                "INSERT INTO gameRules (key, description, date)"
                " VALUES (:key, :description, :date)",
                asdict(rules),
            )

        # Insert game and get id
        for name in players:
            player_key = unique_id()
            postgres_session.execute(
                "INSERT INTO player (key, name)"
                " VALUES (:key, :name)",
                dict(key=player_key, name=name),
            )
            score_history_key = unique_id()
            postgres_session.execute(
                "INSERT INTO playerScoreHistory (key, scores, currentScore, playerKey, gameKey)"
                " VALUES (:key, :scores, :currentScore, :playerKey, :gameKey)",
                dict(key=score_history_key, scores=[], currentScore=0, playerKey=player_key, gameKey=game_key),
            )
            players_added.add(player_key)
        postgres_session.commit()

    yield _add_game

    for game_key in games_added:
        postgres_session.execute(
            "DELETE FROM gameRules WHERE gameKey=:game_key",
            dict(game_key=game_key),
        )
        postgres_session.execute(
            "DELETE FROM playerScoreHistory WHERE gameKey=:game_key",
            dict(game_key=game_key),
        )
        postgres_session.execute(
            "DELETE FROM game WHERE key=:key", dict(key=game_key),
        )
    for player_key in players_added:
        postgres_session.execute(
            "DELETE FROM player WHERE key=:key", dict(key=player_key),
        )
        postgres_session.commit()


@pytest.fixture
def restart_api():
    (Path(__file__).parent / "ok_scoring.py").touch()
    time.sleep(0.5)
    wait_for_webapp_to_come_up()
