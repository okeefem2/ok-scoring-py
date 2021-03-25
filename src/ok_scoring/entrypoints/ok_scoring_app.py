from flask import Flask, request
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
    players = create_players(request.json()['players'])
    rules = create_game_rules(request.json()['rules'])
    game = create_game(request.json()['description'], players, rules)
    return {'game': game}, 201

