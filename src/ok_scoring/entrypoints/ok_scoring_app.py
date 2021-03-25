from flask import Flask, request, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ok_scoring import ok_scoring_config
from ok_scoring.db import orm
from ok_scoring.service.game_rules_service import create_game_rules
from ok_scoring.service.game_service import create_game
from ok_scoring.service.player_service import create_players

orm.start_mappers()
get_session = sessionmaker(bind=create_engine(ok_scoring_config.get_postgres_uri()))
app = Flask(__name__)


@app.route('/', methods=['GET'])
def home():
    return 'Hello OK Scoring', 201


@app.route('/game', methods=['POST'])
def create_game_endpoint():
    try:
        players = create_players(request.json['players'])
        rules = create_game_rules(request.json['rules'])
        game = create_game(description=request.json['description'], players=players, rules=rules)
        return {'game': game}, 201
    except BaseException as e:
        return {'error': "{0}".format(e)}, 500



