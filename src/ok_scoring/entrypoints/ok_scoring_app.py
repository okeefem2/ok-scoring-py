import copy

from flask import Flask, request
from ok_scoring.db.session import db_session
from ok_scoring.entrypoints.v2.routes import api_v2
from ok_scoring.model.validation_error import OKValidationError
from ok_scoring.repository.game_repository import GameRepository
from ok_scoring.repository.player_repository import PlayerRepository
from ok_scoring.service.player_score_history_service import find_by_player_key

from ok_scoring.service.game_rules_service import build_new_game_rules, game_complete
from ok_scoring.service.game_service import validate_and_set_round_score, update_winner, build_new_game, update_dealer
from ok_scoring.service.player_service import create_players


app = Flask(__name__)


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


@app.route('/', methods=['GET'])
def home():
    return 'Hello OK Scoring', 201


@app.route('/games', methods=['POST'])
def create_game_endpoint():
    try:
        session = db_session()
        game_repo = GameRepository(session)
        players_repo = PlayerRepository(session)
        player_names = request.json.get('players')
        existing_players = players_repo.get_by_names(player_names)
        new_players = create_players(player_names, existing_players)
        players_repo.bulk_add(new_players)

        players = new_players + existing_players

        rules = build_new_game_rules(request.json.get('rules'))
        game = build_new_game(description=request.json.get('description'),
                              players=players,
                              rules=rules)
        game_repo.add(game)
        session.commit()
        # Not sure if I need to return players here
        return {'game': game, 'players': players}, 201
    except OKValidationError as e:
        return {'error': e.errors}, 400
    except Exception as e:
        print(e)
        return {'error': "{0}".format(e)}, 500


@app.route('/games/<uuid:game_key>', methods=['GET'])
def fetch_game_endpoint(game_key):
    try:
        session = db_session()
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
        session = db_session()
        repo = PlayerRepository(session)
        players = repo.get_by_game_key(str(game_key))
        if players is None:
            return 404
        return {'players': players}, 200
    except BaseException as e:
        print(e)
        return {'error': "{0}".format(e)}, 500


@app.route('/games/<uuid:game_key>/scores/<uuid:player_key>', methods=['POST'])
def set_player_round_score(game_key, player_key):
    try:
        session = db_session()
        game_repo = GameRepository(session)

        score = int(request.json.get('score'))
        score_index_json = request.json.get('score_index')
        score_index = int(score_index_json) if score_index_json is not None else 0
        try:
            round_index = int(request.json.get('round_index'))
        except Exception as e:
            return {'error': 'round_index must be a valid int'}, 422

        game = game_repo.get(str(game_key))

        # TODO service these
        player_score_history = find_by_player_key(game.scoreHistory, player_key)

        # TODO this needs to be a new service validation
        # Can add round to game vs can add round for player
        if round_index >= len(player_score_history.scores) and game_complete(game.rules, game.scoreHistory):
            return {'error': 'Cannot add a new round to a complete game'}, 422

        # TODO I think I need to have all the scores load here
        previous_score_history = copy.deepcopy(game.scoreHistory)

        player_score_history = \
            validate_and_set_round_score(score_history=player_score_history,
                                         rules=game.rules,
                                         score=score,
                                         score_index=score_index,
                                         round_index=round_index
                                         )

        game.scoreHistory = [player_score_history if s.playerKey == player_key else s for s in game.scoreHistory]
        update_winner(game)
        update_dealer(new_game=game, round_index=round_index, previous_score_history=previous_score_history)
        session.commit()

        return {'game': game}, 200
    except BaseException as e:
        print(e)
        return {'error': "{0}".format(e)}, 500


# V2 endpoints

app.register_blueprint(api_v2, url_prefix='/v2')


