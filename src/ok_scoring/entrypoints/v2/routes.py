import copy

from flask import request, Blueprint
from jsonschema_rs import ValidationError
from ok_scoring.db.session import db_session
from ok_scoring.model.validation_error import OKValidationError
from ok_scoring.repository.game_repository import GameRepository
from ok_scoring.repository.player_repository import PlayerRepository
from ok_scoring.service.game_rules_service import build_new_game_rules_v2
from ok_scoring.service.game_rules_service_v2 import can_add_round, validate_game_state
from ok_scoring.service.game_service import build_new_game, update_winner_v2, update_dealer_v2
from ok_scoring.service.player_score_history_service import set_round_score, find_by_player_key
from ok_scoring.service.player_service import create_players


api_v2 = Blueprint('v2', __name__)


@api_v2.route('/games', methods=['POST'])
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
        rules = build_new_game_rules_v2(request.json.get('rules'))
        game = build_new_game(description=request.json.get('description'),
                              players=players,
                              rulesV2=rules)
        game_repo.add(game)
        session.commit()
        # Not sure if I need to return players here
        return {'game': game, 'players': players}, 201
    except OKValidationError as e:
        return {'error': e.errors}, 400
    except Exception as e:
        print(e)
        return {'error': "{0}".format(e)}, 500


# TODO could consider a POST vs PUT workflow
@api_v2.route('/games/<uuid:game_key>/scores/<uuid:player_key>', methods=['POST'])
def set_player_round_score_v2_endpoint(game_key, player_key):
    try:
        session = db_session()
        game_repo = GameRepository(session)

        score = int(request.json.get('score'))
        score_index_json = request.json.get('score_index')
        score_index = int(score_index_json) if score_index_json is not None else 0
        try:
            round_index = int(request.json.get('round_index'))
        except ValueError:
            return {'error': 'round_index must be a valid int'}, 422

        game = game_repo.get(str(game_key))
        player_score_history = find_by_player_key(game.scoreHistory, player_key)

        if can_add_round(round_index, player_score_history, game):
            return {'error': 'Cannot add a new round to a complete game'}, 422

        previous_score_history = copy.deepcopy(game.scoreHistory)

        player_score_history = \
            set_round_score(score_history=player_score_history,
                            score=score,
                            score_index=score_index,
                            round_index=round_index
                            )

        game.scoreHistory = [player_score_history if s.playerKey == player_key else s for s in game.scoreHistory]

        try:
            validate_game_state(game)
        except ValidationError as e:
            return e, 422
        update_winner_v2(game)
        update_dealer_v2(new_game=game, round_index=round_index, previous_score_history=previous_score_history)
        session.commit()

        return {'game': game}, 200
    except BaseException as e:
        print(e)
        return {'error': "{0}".format(e)}, 500
