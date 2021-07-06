from flask import Flask, request
from ok_scoring.model.validation_error import ValidationError
from ok_scoring.repository.game_repository import GameRepository
from ok_scoring.repository.game_rules_repository import GameRulesRepository
from ok_scoring.repository.player_repository import PlayerRepository
from ok_scoring.repository.player_score_history_repository import PlayerScoreHistoryRepository
from ok_scoring.service.player_score_history_service import set_round_score
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ok_scoring import ok_scoring_config
from ok_scoring.db import orm
from ok_scoring.service.game_rules_service import create_game_rules, determine_winner
from ok_scoring.service.game_service import create_game, save_round_score, update_winner
from ok_scoring.service.player_service import create_players
from uuid import uuid4, UUID

orm.start_mappers()
get_session = sessionmaker(
    bind=create_engine(ok_scoring_config.get_postgres_uri()),
)
app = Flask(__name__)


@app.route('/', methods=['GET'])
def home():
    return 'Hello OK Scoring', 201


@app.route('/games', methods=['POST'])
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
        return {'game': game, 'players': players}, 201
    except ValidationError as e:
        return {'error': e.errors}, 400
    except Exception as e:
        print(e)
        return {'error': "{0}".format(e)}, 500


@app.route('/games/<uuid:game_key>', methods=['GET'])
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


@app.route('/games/<uuid:game_key>/players', methods=['GET'])
def fetch_players_for_game(game_key):
    try:
        session = get_session()
        repo = PlayerRepository(session)
        print('fetching players!')
        players = repo.get_by_game_key(str(game_key))
        if players is None:
            return 404
        return {'players': players}, 200
    except BaseException as e:
        print(e)
        return {'error': "{0}".format(e)}, 500


# TODO look into a decorator middleware thing for this...
# basically to say "recalculate winning player after this is done"
@app.route('/games/<uuid:game_key>/scores/<uuid:player_key>', methods=['POST'])
def set_player_round_score(game_key, player_key):
    try:
        session = get_session()
        game_repo = GameRepository(session)
        player_score_history_repo = PlayerScoreHistoryRepository(session)

        score = int(request.json.get('score'))
        score_index = int(request.json.get('score_index'))
        game = game_repo.get(str(game_key))
        print('game score history', game.scoreHistory)

        player_score_history = next((score for score in game.scoreHistory if str(score.playerKey) == str(player_key)), None)
        print('player_score_history to update', player_score_history)

        player_score_history = save_round_score(player_score_history, game.rules, score, score_index)
        print('updated player_score_history', player_score_history)

        game.scoreHistory = [player_score_history if str(s.playerKey) == str(player_key) else s for s in game.scoreHistory]
        update_winner(game)
        session.commit()
        return {'game': game}, 200
    except BaseException as e:
        print(e)
        return {'error': "{0}".format(e)}, 500

