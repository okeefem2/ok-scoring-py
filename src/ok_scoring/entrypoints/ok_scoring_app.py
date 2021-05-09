from flask import Flask, request
from ok_scoring.model.validation_error import ValidationError
from ok_scoring.repository.game_repository import GameRepository
from ok_scoring.repository.game_rules_repository import GameRulesRepository
from ok_scoring.repository.player_repository import PlayerRepository
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ok_scoring import ok_scoring_config
from ok_scoring.db import orm
from ok_scoring.service.game_rules_service import create_game_rules
from ok_scoring.service.game_service import create_game
from ok_scoring.service.player_service import create_players

orm.start_mappers()
get_session = sessionmaker(
    bind=create_engine(ok_scoring_config.get_postgres_uri()),
)
app = Flask(__name__)


@app.route('/', methods=['GET'])
def home():
    return 'Hello OK Scoring', 201


@app.route('/game', methods=['POST'])
def create_game_endpoint():
    try:
        session = get_session()
        game_repo = GameRepository(session)
        players_repo = PlayerRepository(session)
        rules_repo = GameRulesRepository(session)
        players = create_players(players_repo, request.json.get('players'))
        rules = create_game_rules(rules_repo, request.json.get('rules'))
        game = create_game(repo=game_repo,
                           description=request.json.get('description'),
                           players=players,
                           rules=rules
                           )
        session.commit()
        return {'game': game}, 201
    except ValidationError as e:
        return {'error': e.errors}, 400
    except Exception as e:
        print(e)
        return {'error': "{0}".format(e)}, 500


@app.route('/game/<uuid:game_key>', methods=['GET'])
def fetch_game_endpoint(game_key):
    try:
        session = get_session()
        repo = GameRepository(session)
        game = repo.get(str(game_key))
        if game is None:
            return 404
        return {'game': game}, 200
    except BaseException as e:
        return {'error': "{0}".format(e)}, 500
